import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import pandas as pd

def calculate_psnr(hr_img, sr_img):
    """计算 PSNR（峰值信噪比）"""
    # 确保图像数据类型一致
    hr_img = hr_img.astype(np.float64)
    sr_img = sr_img.astype(np.float64)
    
    mse = np.mean((hr_img - sr_img) **2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr

def calculate_ssim(hr_img, sr_img):
    """计算 SSIM（结构相似性）"""
    # 确保图像为灰度图
    if len(hr_img.shape) > 2:
        hr_img_gray = cv2.cvtColor(hr_img, cv2.COLOR_BGR2GRAY)
    else:
        hr_img_gray = hr_img
    if len(sr_img.shape) > 2:
        sr_img_gray = cv2.cvtColor(sr_img, cv2.COLOR_BGR2GRAY)
    else:
        sr_img_gray = sr_img
    
    # 确保图像尺寸相同
    if hr_img_gray.shape != sr_img_gray.shape:
        sr_img_gray = cv2.resize(sr_img_gray, (hr_img_gray.shape[1], hr_img_gray.shape[0]))
    
    return ssim(hr_img_gray, sr_img_gray, data_range=sr_img_gray.max() - sr_img_gray.min())

def find_sr_file(hr_filename, sr_folder, algorithm_name):
    """更智能地查找超分图像文件"""
    # 尝试多种可能的文件名格式
    base_name, ext = os.path.splitext(hr_filename)
    
    # 尝试原文件名 + "_算法名称" + 扩展名
    possible_names = [
        f"{base_name}_{algorithm_name}{ext}",
        f"{base_name}{ext.replace('.', f'_{algorithm_name}.')}"  # 原始格式
    ]
    
    # 检查可能的文件名
    for name in possible_names:
        sr_path = os.path.join(sr_folder, name)
        if os.path.exists(sr_path):
            return sr_path
    
    # 如果找不到，尝试更宽松的匹配（包含算法名即可）
    for file in os.listdir(sr_folder):
        if base_name in file and algorithm_name in file and ext in file:
            return os.path.join(sr_folder, file)
    
    return None

def process_images(hr_folder, sr_folder, excel_output_path, algorithm_name):
    """处理图像并计算指标"""
    # 获取HR文件夹中的所有图片文件
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tif']
    hr_files = [f for f in os.listdir(hr_folder) 
               if os.path.splitext(f)[1].lower() in image_extensions]
    
    data = []
    category_data = {}
    total_processed = 0
    total_skipped = 0

    print(f"开始处理图像，HR文件夹: {hr_folder}")
    print(f"超分图像文件夹: {sr_folder}")
    print(f"算法名称: {algorithm_name}\n")

    for hr_file in hr_files:
        hr_img_path = os.path.join(hr_folder, hr_file)
        
        # 查找对应的超分图像
        sr_img_path = find_sr_file(hr_file, sr_folder, algorithm_name)
        
        if not sr_img_path:
            print(f"警告: 未找到对应的超分图像，跳过 {hr_file}")
            total_skipped += 1
            continue

        # 读取图像
        try:
            hr_img = cv2.imread(hr_img_path)
            sr_img = cv2.imread(sr_img_path)
            
            if hr_img is None:
                print(f"警告: 无法读取HR图像 {hr_file}")
                total_skipped += 1
                continue
                
            if sr_img is None:
                print(f"警告: 无法读取超分图像 {os.path.basename(sr_img_path)}")
                total_skipped += 1
                continue
        except Exception as e:
            print(f"读取图像时出错 {hr_file}: {str(e)}")
            total_skipped += 1
            continue

        # 确保两张图片尺寸相同
        if hr_img.shape != sr_img.shape:
            print(f"调整尺寸: {os.path.basename(sr_img_path)} 匹配 {hr_file}")
            sr_img = cv2.resize(sr_img, (hr_img.shape[1], hr_img.shape[0]))

        # 计算指标
        try:
            psnr_val = calculate_psnr(hr_img, sr_img)
            ssim_val = calculate_ssim(hr_img, sr_img)
            
            # 保留两位小数
            psnr_val = round(psnr_val, 2)
            ssim_val = round(ssim_val, 4)
            
            # 在终端输出结果
            print(f"处理 {hr_file}: PSNR = {psnr_val}, SSIM = {ssim_val}")
            
            data.append({
                'HR_Image': hr_file,
                'SR_Image': os.path.basename(sr_img_path),
                'PSNR': psnr_val,
                'SSIM': ssim_val
            })
            
            # 提取类别（假设文件名中第一个下划线前的部分为类别）
            category = hr_file.split('_')[0]
            if category not in category_data:
                category_data[category] = {'psnr_sum': 0, 'ssim_sum': 0, 'count': 0}
            category_data[category]['psnr_sum'] += psnr_val
            category_data[category]['ssim_sum'] += ssim_val
            category_data[category]['count'] += 1
            
            total_processed += 1
            
        except Exception as e:
            print(f"计算指标时出错 {hr_file}: {str(e)}")
            total_skipped += 1
            continue

    # 生成Excel文件，包含两个工作表
    with pd.ExcelWriter(excel_output_path, engine='openpyxl') as writer:
        # 单张图片的指标
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name='Image_Metrics', index=False)
        
        # 类别的平均指标
        category_rows = []
        for category, info in category_data.items():
            avg_psnr = round(info['psnr_sum'] / info['count'], 2)
            avg_ssim = round(info['ssim_sum'] / info['count'], 4)
            category_rows.append({
                'Category': category,
                'Average_PSNR': avg_psnr,
                'Average_SSIM': avg_ssim,
                'Image_Count': info['count']
            })
        
        # 添加总体平均值
        if data:
            overall_avg_psnr = round(sum(item['PSNR'] for item in data) / len(data), 2)
            overall_avg_ssim = round(sum(item['SSIM'] for item in data) / len(data), 4)
            category_rows.append({
                'Category': 'Overall',
                'Average_PSNR': overall_avg_psnr,
                'Average_SSIM': overall_avg_ssim,
                'Image_Count': len(data)
            })
        
        category_df = pd.DataFrame(category_rows)
        category_df.to_excel(writer, sheet_name='Category_Averages', index=False)

    # 输出统计信息
    print("\n" + "="*50)
    print(f"处理完成! 共处理 {total_processed} 张图像，跳过 {total_skipped} 张图像")
    print(f"结果已保存到 {excel_output_path}")
    print(f"包含两个工作表: 'Image_Metrics' 和 'Category_Averages'")
    print("="*50)

# 示例调用
if __name__ == "__main__":
    hr_folder = r'E:\Mamba-CV\SR-DATA\RSSCN7\val\HR'  # 标准 HR 图片文件夹路径
    sr_folder = r"D:\Wz_Project_Learning\Mamba-CV\MambaIR\inference_results\inference_results\DFSMamba_RSSCN7_x2"  # 超分重建后图片文件夹路径
    excel_output = r'D:\Wz_Project_Learning\Mamba-CV\MambaIR\inference_results\inference_excel\DFSMamba_RSSCN7_x2_results.xlsx'  # 合并后的Excel文件名
    algorithm_name = 'DFSMamba'  # 算法名称

    process_images(hr_folder, sr_folder, excel_output, algorithm_name)
