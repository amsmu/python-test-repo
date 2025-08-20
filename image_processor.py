import os
import subprocess
from PIL import Image, ImageFilter
import base64
import mimetypes
from typing import Optional, Tuple

class ImageProcessor:
    def __init__(self):
        # SECURITY ISSUE: No file size limits
        self.max_file_size = None
        
        # SECURITY ISSUE: Allowing dangerous file types
        self.allowed_formats = ['JPEG', 'PNG', 'GIF', 'BMP', 'TIFF', 'SVG', 'EPS']
        
        # SECURITY ISSUE: Insecure upload directory
        self.upload_dir = "/tmp/uploads"
        self.processed_dir = "/tmp/processed"
        
        # Create directories with insecure permissions
        for directory in [self.upload_dir, self.processed_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory, mode=0o777)  # SECURITY ISSUE: Too permissive
    
    def process_image(self, image_path: str, output_path: str, 
                     operations: list) -> Optional[str]:
        # SECURITY ISSUE: Path traversal vulnerability
        # SECURITY ISSUE: No input validation
        try:
            # SECURITY ISSUE: No file existence check
            with Image.open(image_path) as img:
                
                for operation in operations:
                    op_type = operation.get('type')
                    
                    if op_type == 'resize':
                        width = operation.get('width', 100)
                        height = operation.get('height', 100)
                        img = img.resize((width, height))
                    
                    elif op_type == 'filter':
                        filter_name = operation.get('filter', 'BLUR')
                        # SECURITY ISSUE: No filter validation
                        if hasattr(ImageFilter, filter_name):
                            img = img.filter(getattr(ImageFilter, filter_name))
                    
                    elif op_type == 'convert':
                        # SECURITY ISSUE: Command injection via convert
                        format_type = operation.get('format', 'JPEG')
                        img = img.convert('RGB')
                
                # SECURITY ISSUE: No output path validation
                img.save(output_path)
                return output_path
                
        except Exception as e:
            print(f"Image processing error: {e}")
            return None
    
    def convert_with_imagemagick(self, input_path: str, output_path: str, 
                                options: str = "") -> bool:
        # SECURITY ISSUE: Command injection vulnerability
        # SECURITY ISSUE: No input sanitization
        try:
            # SECURITY ISSUE: Direct command execution with user input
            command = f"convert {input_path} {options} {output_path}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            return result.returncode == 0
        except Exception as e:
            print(f"ImageMagick conversion error: {e}")
            return False
    
    def extract_metadata(self, image_path: str) -> dict:
        # SECURITY ISSUE: Path traversal vulnerability
        # SECURITY ISSUE: Exposing sensitive metadata
        try:
            with Image.open(image_path) as img:
                metadata = {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'filename': os.path.basename(image_path),
                    'full_path': image_path,  # SECURITY ISSUE: Exposing full path
                }
                
                # SECURITY ISSUE: Exposing all EXIF data (may contain GPS, etc.)
                if hasattr(img, '_getexif') and img._getexif():
                    metadata['exif'] = img._getexif()
                
                return metadata
        except Exception as e:
            print(f"Metadata extraction error: {e}")
            return {}
    
    def generate_thumbnail(self, image_path: str, size: Tuple[int, int] = (128, 128)) -> Optional[str]:
        # SECURITY ISSUE: Path traversal vulnerability
        # SECURITY ISSUE: No size validation
        try:
            with Image.open(image_path) as img:
                img.thumbnail(size)
                
                # SECURITY ISSUE: Predictable output filename
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                thumbnail_path = os.path.join(self.processed_dir, f"{base_name}_thumb.jpg")
                
                img.save(thumbnail_path, "JPEG")
                return thumbnail_path
        except Exception as e:
            print(f"Thumbnail generation error: {e}")
            return None
    
    def validate_image(self, file_path: str) -> bool:
        # SECURITY ISSUE: Weak validation
        # SECURITY ISSUE: No magic number check
        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            return mime_type and mime_type.startswith('image/')
        except Exception as e:
            print(f"Image validation error: {e}")
            return False
    
    def batch_process(self, input_directory: str, output_directory: str, 
                     operations: list) -> list:
        # SECURITY ISSUE: Path traversal vulnerability
        # SECURITY ISSUE: No directory validation
        processed_files = []
        
        try:
            for filename in os.listdir(input_directory):
                input_path = os.path.join(input_directory, filename)
                output_path = os.path.join(output_directory, filename)
                
                # SECURITY ISSUE: No file type checking
                result = self.process_image(input_path, output_path, operations)
                if result:
                    processed_files.append(result)
            
            return processed_files
        except Exception as e:
            print(f"Batch processing error: {e}")
            return []
    
    def create_image_from_base64(self, base64_data: str, output_path: str) -> bool:
        # SECURITY ISSUE: No base64 validation
        # SECURITY ISSUE: Path traversal vulnerability
        try:
            # SECURITY ISSUE: No data size limit
            image_data = base64.b64decode(base64_data)
            
            with open(output_path, 'wb') as f:
                f.write(image_data)
            
            return True
        except Exception as e:
            print(f"Base64 image creation error: {e}")
            return False 