# 1-Month Defect Detection System Plan
## DOBOT Magician + Computer Vision

**Project Goal:** Build a working prototype that sorts foam cubes by quality (color/damage detection) using robotic automation.

**Team:** Solo developer
**Timeline:** 4 weeks
**Hardware:** DOBOT Magician, conveyor belt, USB camera, GPU computer

---

## Week 1: Setup, Integration & Learning
**Goal:** Get all hardware communicating and understand the basics

### Days 1-2: Environment Setup
- [ ] Install DOBOT Magician SDK/API (pydobot or DobotDll)
- [ ] Test basic arm movements with simple Python scripts
- [ ] Document home position and workspace boundaries
- [ ] Install computer vision stack:
  - OpenCV (camera interface)
  - PyTorch or TensorFlow (ML framework)
  - Basic dependencies (numpy, matplotlib, scikit-learn)

### Days 3-4: Camera & Conveyor Integration
- [ ] Mount camera above conveyor belt (fixed position, perpendicular view)
- [ ] Set up proper lighting (even, diffuse lighting to minimize shadows)
- [ ] Test camera capture with OpenCV
- [ ] Calibrate camera position to capture full object as it passes
- [ ] Connect conveyor belt controls to computer (GPIO, relay, or manual for now)
- [ ] Test conveyor speed and determine optimal speed for imaging

### Days 5-7: Basic Object Detection & Tracking
- [ ] Implement background subtraction to detect objects on conveyor
- [ ] Use blob detection or contour detection to identify cube position
- [ ] Test coordinate transformation: camera pixels → robot arm coordinates
- [ ] Create simple "pick and place" routine:
  - Detect object position
  - Stop conveyor (or time the grab)
  - Move arm to pick up object
  - Place in predefined location (good/bad bins)
- [ ] Validate basic workflow WITHOUT defect detection (all objects go to "good" bin)

**Week 1 Deliverable:** System can detect, pick, and place foam cubes consistently

---

## Week 2: Data Collection & ML Model Training
**Goal:** Build dataset and train initial defect classifier

### Days 8-10: Data Collection
- [ ] Set up data collection pipeline:
  - Capture images when object detected
  - Save with timestamp and labels
  - Create folder structure: `data/good/`, `data/defective_color/`, `data/defective_damage/`
- [ ] Create variety of defective samples:
  - Color defects: paint, mark, or use different colored cubes
  - Damage defects: crush, tear, or dent cubes
- [ ] Collect balanced dataset:
  - Target: 200-300 images per class minimum
  - 150 good cubes
  - 100 color defects
  - 100 damage defects
- [ ] Implement simple labeling tool or use manual file organization
- [ ] Split data: 70% train, 15% validation, 15% test

### Days 11-14: Model Development
- [ ] Start with **transfer learning** approach (beginner-friendly):
  - Use pre-trained model (ResNet18, MobileNetV2, or EfficientNet-B0)
  - Fine-tune on your foam cube dataset
  - Start with binary classification (good vs defective)
- [ ] Set up training pipeline:
  - Data augmentation (rotation, brightness, contrast)
  - Training loop with validation
  - Save best model checkpoints
- [ ] Train initial model and evaluate:
  - Target: >85% accuracy for Week 2 (will improve later)
  - Analyze confusion matrix
  - Identify which defect types are hardest to detect
- [ ] Export model for inference (ONNX or TorchScript for speed)
- [ ] Create inference script that loads model and classifies images

**Week 2 Deliverable:** Trained ML model that can classify foam cubes with >85% accuracy

---

## Week 3: Full System Integration
**Goal:** Integrate ML model with robotic sorting system

### Days 15-17: Real-time Detection Pipeline
- [ ] Integrate ML model into main control loop:
  ```
  1. Detect object on conveyor (OpenCV)
  2. Capture image of object
  3. Run ML inference
  4. Get classification (good/defective + confidence score)
  5. Trigger appropriate robot action
  ```
- [ ] Implement decision logic:
  - If confidence > 90% good → sort to "good" bin
  - If confidence > 90% defective → sort to "defective" bin
  - If confidence < 90% → sort to "uncertain" bin (manual review)
- [ ] Optimize inference speed:
  - Target: <200ms per classification
  - Use GPU if available
  - Consider model quantization if too slow

### Days 18-21: Testing & Calibration
- [ ] Run end-to-end tests with 50+ cubes
- [ ] Measure system performance:
  - Accuracy (% correctly sorted)
  - False positive rate (good cubes marked defective)
  - False negative rate (defective cubes marked good)
  - Processing speed (cubes per minute)
- [ ] Fine-tune pick-and-place positions
- [ ] Adjust confidence thresholds based on test results
- [ ] Handle edge cases:
  - Multiple objects detected
  - No object detected
  - Object dropped during pick
  - Arm collision avoidance
- [ ] Implement basic logging system to track decisions

**Week 3 Deliverable:** Fully integrated system sorting cubes with >80% accuracy

---

## Week 4: Refinement & Phase 2 Preparation
**Goal:** Improve performance and prepare for washer detection

### Days 22-24: Performance Improvements
- [ ] Analyze failure cases from Week 3 testing
- [ ] Collect additional training data for difficult cases
- [ ] Retrain model with expanded dataset
- [ ] Experiment with multi-class classification:
  - Class 0: Good
  - Class 1: Color defect
  - Class 2: Damage defect
  - (Helps understand which defect types are present)
- [ ] Improve lighting/camera setup if needed
- [ ] Optimize conveyor speed vs accuracy tradeoff

### Days 25-26: Documentation & Reliability
- [ ] Create system documentation:
  - Hardware setup diagram
  - Calibration procedures
  - Model retraining guide
  - Troubleshooting common issues
- [ ] Add error handling and recovery:
  - Camera disconnection
  - Arm position errors
  - Conveyor belt issues
- [ ] Implement emergency stop functionality
- [ ] Create simple GUI or status display (optional but helpful)

### Days 27-28: Phase 2 Scoping (Washer Detection)
- [ ] Analyze new requirements for washer detection:
  - Washer presence detection (missing washer)
  - Washer alignment (crooked/misaligned)
  - Glue quality (if visible)
- [ ] Determine if current model architecture can extend or needs redesign:
  - Option A: Add new classes to existing model
  - Option B: Two-stage detection (cube quality → washer quality)
  - Option C: Object detection approach (YOLO/SSD to locate washer)
- [ ] Create initial samples of cubes with washers (good and defective)
- [ ] Capture test images to assess difficulty level
- [ ] Document Phase 2 plan based on learnings from Phase 1

**Week 4 Deliverable:** Refined system with >90% accuracy, documented, and Phase 2 roadmap

---

## Key Technologies & Tools

### DOBOT Control
- **pydobot** library (Python): Easiest for beginners
- Alternative: Official DOBOT SDK/API
- Learn: Basic kinematics, gripper control, position commands

### Computer Vision
- **OpenCV**: Object detection, tracking, camera interface
- **PIL/Pillow**: Image preprocessing

### Machine Learning
- **PyTorch** or **TensorFlow/Keras**: Deep learning framework
- **timm** (PyTorch Image Models): Pre-trained models
- **albumentations**: Data augmentation
- Start with: Transfer learning from ImageNet models

### Development
- **Python 3.8+**: Primary language
- **Jupyter notebooks**: Experimentation and visualization
- **Git**: Version control for code and experiment tracking

---

## Success Metrics

### End of Month 1:
- ✅ System reliably picks and places objects (>95% success rate)
- ✅ Defect detection accuracy >90% on test set
- ✅ Processing speed: 5-10 cubes per minute minimum
- ✅ False positive rate: <10%
- ✅ System runs for 30 minutes without intervention
- ✅ Clear documentation for retraining and calibration

---

## Risk Mitigation

### Technical Risks:
1. **Camera positioning/lighting issues** → Allocate extra time in Week 1 for calibration
2. **Insufficient training data** → Use data augmentation aggressively
3. **Slow inference speed** → Start with lightweight models (MobileNet)
4. **Robot calibration drift** → Implement regular homing routine

### Scope Risks:
1. **Week 1 takes too long** → Simplify by using manual conveyor control initially
2. **ML model not converging** → Fall back to classical CV methods (color thresholding) temporarily
3. **Integration issues** → Build modular code with clear interfaces for easier debugging

---

## Daily Work Structure (Recommended)

**Morning (3-4 hours):**
- Focus on main development tasks
- Deep work on ML training or integration coding

**Afternoon (2-3 hours):**
- Testing and debugging
- Data collection and labeling
- Documentation

**Evening (1 hour):**
- Learning/research (tutorials, documentation)
- Planning next day's tasks

**Total: ~6-8 hours/day for 20-25 working days**

---

## Resources to Study

### Week 1 Resources:
- DOBOT Magician Python API documentation
- OpenCV object detection tutorials
- Basic robot kinematics

### Week 2 Resources:
- Transfer learning tutorials (PyTorch or TensorFlow)
- Image classification best practices
- Data augmentation techniques

### Week 3-4 Resources:
- Production ML deployment
- Real-time inference optimization
- Error handling in robotic systems

---

## Phase 2 Preview (Month 2)

After completing Month 1 with foam cubes, Phase 2 will add washer detection:

1. **Data collection** for cubes with washers (good vs defective)
2. **Enhanced model** to detect:
   - Missing washers
   - Crooked/misaligned washers
   - Poor glue application (if visible)
3. **Two-stage classification** or object detection approach
4. **Higher precision required** → May need higher resolution camera or closer inspection position

---

## Getting Started - First Steps Tomorrow

1. Clone this repository or create project structure:
   ```
   DOBOT/
   ├── src/
   │   ├── robot_control.py
   │   ├── camera.py
   │   ├── detection.py
   │   └── main.py
   ├── data/
   │   ├── raw/
   │   ├── train/
   │   └── test/
   ├── models/
   ├── notebooks/
   └── docs/
   ```

2. Install pydobot: `pip install pydobot`
3. Test DOBOT connection with simple movement script
4. Verify camera with OpenCV test capture

**You've got this! Start simple, iterate quickly, and don't be afraid to ask questions along the way.**
