# DOBOT Defect Detection System

Computer vision-based defect detection system using DOBOT Magician robotic arm for automated quality control.

## Project Overview

This system uses a DOBOT Magician robotic arm combined with computer vision and machine learning to automatically detect and sort defective products on a conveyor belt.

**Current Phase:** Foam cube defect detection (color and damage)
**Future Phase:** Foam cubes with washers (alignment and presence detection)

## Hardware Requirements

- DOBOT Magician robotic arm
- Conveyor belt
- USB webcam (mounted above conveyor)
- Computer with:
  - NVIDIA GPU (recommended for ML training)
  - USB ports for camera and DOBOT
  - Linux/Windows/macOS

## Software Setup

### 1. Install Python 3.8+

Verify Python installation:
```bash
python --version
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** If you have an NVIDIA GPU, ensure you have CUDA installed for PyTorch GPU support. Visit [PyTorch website](https://pytorch.org/get-started/locally/) for GPU-specific installation instructions.

### 4. Test Camera

```bash
python src/camera_test.py
```

This will:
- Detect available cameras
- Show live camera feed
- Test object detection capabilities
- Allow you to save test images

**Controls:**
- `q` - Quit
- `s` - Save current frame
- `b` - Toggle background subtraction
- `c` - Toggle contour detection
- `r` - Reset background model

### 5. Test DOBOT Connection (Coming Soon)

```bash
python src/robot_test.py
```

## Project Structure

```
DOBOT/
├── src/                          # Source code
│   ├── camera_test.py           # Camera testing and validation
│   ├── robot_control.py         # DOBOT arm control (to be created)
│   ├── detection.py             # Object detection logic (to be created)
│   └── main.py                  # Main integration script (to be created)
├── data/                         # Dataset storage
│   ├── raw/                     # Raw captured images
│   ├── train/                   # Training data
│   │   ├── good/
│   │   ├── defective_color/
│   │   └── defective_damage/
│   ├── validation/              # Validation data
│   └── test/                    # Test data
├── models/                       # Saved ML models
├── notebooks/                    # Jupyter notebooks for experimentation
├── docs/                         # Documentation
├── logs/                         # System logs
├── requirements.txt              # Python dependencies
├── 1_MONTH_PLAN.md              # Detailed 4-week implementation plan
└── README.md                     # This file
```

## Quick Start Guide

### Week 1: Getting Started

1. **Test your camera:**
   ```bash
   python src/camera_test.py
   ```

2. **Position your hardware:**
   - Mount camera above conveyor belt (perpendicular view)
   - Ensure even lighting (minimize shadows)
   - Connect DOBOT to computer via USB

3. **Test DOBOT connection** (script coming next)

### Week 2: Data Collection

1. Create variety of foam cube samples (good and defective)
2. Use camera_test.py to capture images (press 's' to save)
3. Manually organize images into folders:
   - `data/train/good/`
   - `data/train/defective_color/`
   - `data/train/defective_damage/`

### Week 3: Train ML Model

(Training scripts to be added)

### Week 4: Full Integration

(Integration scripts to be added)

## Current Status

- [x] Project structure created
- [x] Requirements defined
- [x] Camera test script ready
- [ ] DOBOT control script
- [ ] Object detection implementation
- [ ] ML training pipeline
- [ ] Full system integration

## Troubleshooting

### Camera Issues

**Camera not detected:**
- Check USB connection
- Try different USB port
- Verify camera works in other applications
- Check permissions (Linux: add user to `video` group)

**Poor image quality:**
- Adjust lighting (even, diffuse light is best)
- Check camera focus
- Try different resolution in camera_test.py

### DOBOT Issues

(To be added after robot_test.py is created)

### Installation Issues

**PyTorch CUDA not available:**
- Verify NVIDIA drivers installed
- Check CUDA toolkit version compatibility
- Reinstall PyTorch with correct CUDA version

**pydobot installation fails:**
- Try: `pip install pydobot --no-cache-dir`
- Check Python version (3.8+ required)

## Resources

- [DOBOT Magician Documentation](https://www.dobot.cc/dobot-magician/product-overview.html)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Transfer Learning Guide](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)

## Next Steps

Follow the detailed plan in `1_MONTH_PLAN.md` for week-by-week guidance.

**Immediate next task:** Test camera setup using `src/camera_test.py`

## License

This project is for educational and prototyping purposes.
