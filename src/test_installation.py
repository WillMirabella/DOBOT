"""
Installation Verification Script
Tests that all major dependencies are installed and working correctly.
"""

import sys


def test_imports():
    """Test importing all major packages"""
    print("Testing package imports...\n")

    packages = [
        ("OpenCV", "cv2"),
        ("NumPy", "numpy"),
        ("PyTorch", "torch"),
        ("TorchVision", "torchvision"),
        ("PIL/Pillow", "PIL"),
        ("scikit-learn", "sklearn"),
        ("matplotlib", "matplotlib"),
        ("pandas", "pandas"),
        ("pydobot", "pydobot"),
        ("timm", "timm"),
        ("albumentations", "albumentations"),
    ]

    results = []
    for name, module in packages:
        try:
            exec(f"import {module}")
            version = eval(f"{module}.__version__")
            results.append((name, "✓", version))
            print(f"✓ {name:20s} v{version}")
        except ImportError as e:
            results.append((name, "✗", str(e)))
            print(f"✗ {name:20s} FAILED: {e}")
        except AttributeError:
            # Some modules don't have __version__
            results.append((name, "✓", "installed"))
            print(f"✓ {name:20s} (version unknown)")

    return results


def test_torch_cuda():
    """Check if PyTorch can access CUDA GPU"""
    print("\n" + "="*50)
    print("PyTorch GPU Check")
    print("="*50)

    try:
        import torch

        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")

        if torch.cuda.is_available():
            print(f"CUDA version: {torch.version.cuda}")
            print(f"GPU device: {torch.cuda.get_device_name(0)}")
            print(f"GPU count: {torch.cuda.device_count()}")

            # Test a simple operation on GPU
            x = torch.rand(3, 3).cuda()
            print(f"✓ Successfully created tensor on GPU")
        else:
            print("⚠ GPU not available - will use CPU for training")
            print("  (This is fine for prototyping, but training will be slower)")

    except Exception as e:
        print(f"✗ Error checking CUDA: {e}")


def test_camera():
    """Quick check if a camera is available"""
    print("\n" + "="*50)
    print("Camera Detection")
    print("="*50)

    try:
        import cv2

        # Try to open default camera
        cap = cv2.VideoCapture(0)

        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                height, width = frame.shape[:2]
                print(f"✓ Camera 0 detected: {width}x{height}")
            else:
                print("⚠ Camera 0 opened but couldn't read frame")
            cap.release()
        else:
            print("✗ No camera detected at index 0")
            print("  Run 'python src/camera_test.py' for detailed camera testing")

    except Exception as e:
        print(f"✗ Error testing camera: {e}")


def main():
    print("="*50)
    print("DOBOT Project - Installation Verification")
    print("="*50)
    print()

    # Test all imports
    results = test_imports()

    # Test PyTorch CUDA
    test_torch_cuda()

    # Test camera
    test_camera()

    # Summary
    print("\n" + "="*50)
    print("Summary")
    print("="*50)

    success_count = sum(1 for _, status, _ in results if status == "✓")
    total_count = len(results)

    print(f"Packages: {success_count}/{total_count} working")

    if success_count == total_count:
        print("\n✓ All systems ready! You can start developing.")
        print("\nNext steps:")
        print("  1. Run: python src/camera_test.py")
        print("  2. Connect and test DOBOT arm")
        print("  3. Follow 1_MONTH_PLAN.md")
    else:
        print("\n⚠ Some packages had issues. Check errors above.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
