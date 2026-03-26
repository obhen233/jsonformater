import PyInstaller.__main__
import os
import sys
import shutil

def build_exe():
    """打包成exe文件，正确设置图标"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # 图标文件路径
    icon_file = 'icon.ico'
    if not os.path.exists(icon_file):
        print(f"警告: 未找到图标文件 {icon_file}")
        print("请将 icon.ico 文件放在当前目录下")
        icon_arg = []
    else:
        icon_arg = ['--icon', icon_file]
        print(f"使用图标文件: {icon_file}")
    
    # 清理之前的构建
    dist_dir = os.path.join(current_dir, 'dist')
    build_dir = os.path.join(current_dir, 'build')
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    
    # PyInstaller参数
    args = [
        'json_formatter.py',
        '--onefile',  # 打包成单个文件
        '--windowed',  # 不显示控制台窗口
        '--name=JSON格式化工具',  # 输出文件名
        '--noconsole',  # 不显示控制台
        '--clean',  # 清理临时文件
        '--uac-admin',  # 如果需要管理员权限
    ] + icon_arg
    
    # 添加数据文件（将图标文件打包进去）
    if os.path.exists(icon_file):
        args.extend(['--add-data', f'{icon_file}{os.pathsep}.'])
    
    print("=" * 50)
    print("开始打包 JSON 格式化工具...")
    print(f"当前目录: {current_dir}")
    print(f"图标文件: {icon_file if os.path.exists(icon_file) else '未找到'}")
    print(f"打包参数: {args}")
    print("=" * 50)
    
    try:
        PyInstaller.__main__.run(args)
        print("\n" + "=" * 50)
        print("打包完成！")
        exe_path = os.path.join(current_dir, 'dist', 'JSON格式化工具.exe')
        if os.path.exists(exe_path):
            print(f"✅ 生成的exe文件: {exe_path}")
            print(f"📦 文件大小: {os.path.getsize(exe_path) / 1024 / 1024:.2f} MB")
            
            # 复制图标文件到dist目录（可选）
            if os.path.exists(icon_file):
                shutil.copy2(icon_file, os.path.join(current_dir, 'dist', 'icon.ico'))
                print(f"📷 图标文件已复制到: {os.path.join(current_dir, 'dist', 'icon.ico')}")
        else:
            print("❌ 打包失败，未找到生成的exe文件")
        print("=" * 50)
    except Exception as e:
        print(f"❌ 打包失败: {e}")
        import traceback
        traceback.print_exc()

def create_ico_placeholder():
    """创建一个简单的ICO占位文件（如果不存在）"""
    icon_file = 'icon.ico'
    if not os.path.exists(icon_file):
        print("未找到 icon.ico 文件")
        print("请准备一个 icon.ico 文件放在当前目录")
        print("或者使用在线工具将PNG转换为ICO格式")
        print("推荐: https://www.icoconverter.com/")
        return False
    return True

if __name__ == '__main__':
    if create_ico_placeholder():
        build_exe()
    else:
        print("请先准备 icon.ico 文件后再运行打包")
        input("按回车键退出...")