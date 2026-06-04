import torch
import sys

print(f"Python Version: {sys.version}")
print(f"PyTorch Version: {torch.__version__}")
print(f"Is CUDA available?: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA Device Count: {torch.cuda.device_count()}")
    print(f"Current CUDA Device Index: {torch.cuda.current_device()}")
    
    for i in range(torch.cuda.device_count()):
        print(f"    Device [{i}]: {torch.cuda.get_device_name(i)}")
else:
    print("\nGPU not found for PyTorch.")
    # Check if the hardware drivers are missing or if it's a version mismatch
    try:
        import torch.utils.cpp_extension
        print(f"PyTorch built with CUDA version: {torch.version.cuda}") # type: ignore
    except Exception as e:
        print(f"Could not read backend: {e}")