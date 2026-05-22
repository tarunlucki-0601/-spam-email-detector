import shutil
import os

src_dir = r"C:\Users\Tharun lucki\OneDrive\Desktop\project2"
dest_dir = r"C:\Users\Tharun lucki\OneDrive\Documents\GitHub\spam-email-detector"

def copy_files():
    # Ensure destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    
    for item in os.listdir(src_dir):
        # Ignore these folders
        if item in ['.git', 'venv', '__pycache__']:
            continue
            
        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)
        
        try:
            if os.path.isdir(s):
                if not os.path.exists(d):
                    shutil.copytree(s, d)
                else:
                    # if dir exists, copy contents
                    for sub_item in os.listdir(s):
                        sub_s = os.path.join(s, sub_item)
                        sub_d = os.path.join(d, sub_item)
                        if os.path.isdir(sub_s):
                            if not os.path.exists(sub_d):
                                shutil.copytree(sub_s, sub_d)
                        else:
                            shutil.copy2(sub_s, sub_d)
            else:
                shutil.copy2(s, d)
            print(f"Copied {item}")
        except Exception as e:
            print(f"Failed to copy {item}: {e}")

if __name__ == "__main__":
    copy_files()
