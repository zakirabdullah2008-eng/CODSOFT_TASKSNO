# Task 3 - AI Image Captioning

## Objective

To develop an AI-powered image captioning application that combines computer vision and natural language processing to generate descriptive captions for uploaded images.

## Technologies Used

- Python
- Streamlit
- PyTorch
- Torchvision
- Hugging Face Transformers
- ResNet50
- BLIP
- Pillow

## Project Overview

This project allows users to upload an image and automatically generate a natural-language description using pretrained deep learning models.

The application demonstrates the combination of computer vision and natural language processing.

## AI Pipeline

Image
↓
Image Preprocessing
↓
ResNet50 Feature Extraction
↓
Visual Representation
↓
BLIP Transformer
↓
Natural Language Caption
↓
Generated Caption

## Computer Vision

ResNet50 is a pretrained convolutional neural network used in this project as a visual feature extractor.

The final classification layer is removed so that the network can produce a high-level visual representation of the uploaded image.

## Natural Language Processing

A pretrained BLIP (Bootstrapping Language-Image Pre-training) model is used to generate a natural-language caption for the image.

The model analyzes the image and generates a textual description.

## Features

- Image upload
- Image preview
- Automatic caption generation
- ResNet50 visual feature extraction
- BLIP transformer-based caption generation
- Streamlit web interface
- Loading and status messages
- Error handling
- AI processing information

## Application Workflow

1. The user uploads an image.
2. The image is converted into RGB format.
3. ResNet50 processes the image to extract visual features.
4. The BLIP processor prepares the image for caption generation.
5. The BLIP transformer generates the caption.
6. The generated caption is displayed in the application.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
