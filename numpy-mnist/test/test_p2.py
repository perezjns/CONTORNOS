"""
Test suite for MNIST NumPy project.

This module tests the notebook implementation including:
- Data loading and preprocessing
- One-hot encoding
- Normalization and standardization
- Image transformations (noise, binarization, shifting, cropping)
- Data augmentation
"""

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import numpy as np
import pytest


# Fixture to execute notebook once and cache the namespace
@pytest.fixture(scope="module")
def notebook_namespace():
    """Execute the notebook and return its namespace for all tests."""
    import matplotlib.pyplot as plt
    plt.show = lambda: None  # Mock plt.show to prevent display

    # Load the notebook
    with open('p2-mnist-numpy.ipynb', 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Execute the notebook
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {})

    # Create a namespace to store executed variables and functions
    namespace = {}

    # Extract all cells and execute them in a common namespace
    for cell in nb.cells:
        if cell['cell_type'] == 'code':
            try:
                exec(cell['source'], namespace)
            except Exception as e:
                print(f"Error executing cell: {cell['source']}")
                raise

    return namespace


def test_notebook_has_required_variables(notebook_namespace):
    """Test that all required variables and functions are defined in the notebook."""
    required_items = [
        'matrix_first_100_labels',
        'X_train_flat',
        'X_test_flat',
        'plot_image',
        'y_train_onehot',
        'y_test_onehot',
        'X_train_norm',
        'X_train_standardized',
        'X_train_noisy',
        'binarize_image',
        'X_train_binarized',
        'X_train_noisy_binarized',
        'shift_image',
        'X_train_shifted_right_10',
        'find_limits',
        'crop_image_limits',
        'X_train_shifted',
        'X_train_augmented',
    ]

    for item in required_items:
        assert item in notebook_namespace, f"{item} not found in notebook"


def test_matrix_first_100_labels(notebook_namespace):
    """Test the 10x10 matrix of first 100 labels."""
    matrix_first_100_labels = notebook_namespace['matrix_first_100_labels']

    assert matrix_first_100_labels.shape == (10, 10)
    assert matrix_first_100_labels[0, 0] == 5
    assert matrix_first_100_labels[1, 0] == 3
    assert matrix_first_100_labels[9, 9] == 1


def test_flattening(notebook_namespace):
    """Test that images are correctly flattened."""
    X_train_flat = notebook_namespace['X_train_flat']
    X_test_flat = notebook_namespace['X_test_flat']

    assert X_train_flat.shape == (60000, 28 * 28)
    assert X_test_flat.shape == (10000, 28 * 28)


def test_plot_image_function(notebook_namespace):
    """Test that plot_image function works without errors."""
    X_train_flat = notebook_namespace['X_train_flat']
    plot_image = notebook_namespace['plot_image']

    # Should not raise any exception
    plot_image(X_train_flat[0])


def test_onehot_encoding_shape(notebook_namespace):
    """Test one-hot encoding has correct shape."""
    y_train_onehot = notebook_namespace['y_train_onehot']
    y_test_onehot = notebook_namespace['y_test_onehot']

    assert y_train_onehot.shape == (60000, 10)
    assert y_test_onehot.shape == (10000, 10)


def test_onehot_encoding_values(notebook_namespace):
    """Test one-hot encoding has correct values."""
    y_train_onehot = notebook_namespace['y_train_onehot']
    y_train = notebook_namespace['y_train']

    # Check specific examples
    assert y_train_onehot[0, 5] == 1
    assert y_train_onehot[1, 0] == 1
    assert y_train_onehot[99, 1] == 1

    # Check that correct positions are 1 for first 5 samples
    assert y_train_onehot[range(5), y_train[:5]].all()

    # Each row should sum to 1
    assert np.all(y_train_onehot.sum(axis=1) == 1)


def test_normalization_range(notebook_namespace):
    """Test that normalized images are in [0, 1] range."""
    X_train_norm = notebook_namespace['X_train_norm']

    assert X_train_norm.shape == (60000, 28, 28)
    assert X_train_norm.min() == 0
    assert X_train_norm.max() == 1
    assert X_train_norm.dtype in [np.float32, np.float64]


def test_normalization_statistics(notebook_namespace):
    """Test normalization statistics match expected values."""
    X_train_norm = notebook_namespace['X_train_norm']
    pixel_norm_mean = notebook_namespace['pixel_norm_mean']
    pixel_norm_std = notebook_namespace['pixel_norm_std']

    assert np.isclose(pixel_norm_mean, 0.130660)
    assert np.isclose(pixel_norm_std, 0.308107)
    assert np.isclose(X_train_norm.mean(), 0.130660)
    assert np.isclose(X_train_norm.std(), 0.308107)


def test_standardization_properties(notebook_namespace):
    """Test standardized data has mean ~0 and std ~1."""
    X_train_standardized = notebook_namespace['X_train_standardized']

    assert np.isclose(X_train_standardized.mean(), 0)
    assert np.isclose(X_train_standardized.std(), 1)


def test_noisy_images(notebook_namespace):
    """Test that noisy images are within valid range."""
    X_train_noisy = notebook_namespace['X_train_noisy']

    assert X_train_noisy.shape == (60000, 28, 28)
    assert X_train_noisy.min() >= 0
    assert X_train_noisy.max() <= 255


def test_binarize_image_function(notebook_namespace):
    """Test binarize_image function produces binary output."""
    X_train_noisy = notebook_namespace['X_train_noisy']
    binarize_image = notebook_namespace['binarize_image']

    result = binarize_image(X_train_noisy[0], threshold=128)

    assert result.shape == (28, 28)
    assert result.min() == 0
    assert result.max() == 1
    assert set(np.unique(result)) <= {0, 1}


def test_binarized_datasets(notebook_namespace):
    """Test binarized datasets have correct shape and values."""
    X_train_binarized = notebook_namespace['X_train_binarized']
    X_train_noisy_binarized = notebook_namespace['X_train_noisy_binarized']

    # Test X_train_binarized
    assert X_train_binarized.shape == (60000, 28, 28)
    assert X_train_binarized.min() == 0
    assert X_train_binarized.max() == 1
    assert set(np.unique(X_train_binarized)) <= {0, 1}

    # Test X_train_noisy_binarized
    assert X_train_noisy_binarized.shape == (60000, 28, 28)
    assert X_train_noisy_binarized.min() == 0
    assert X_train_noisy_binarized.max() == 1
    assert set(np.unique(X_train_noisy_binarized)) <= {0, 1}


def test_shift_image_function(notebook_namespace):
    """Test shift_image function preserves shape."""
    X_train = notebook_namespace['X_train']
    shift_image = notebook_namespace['shift_image']

    original_shape = X_train[0].shape
    shifted = shift_image(X_train[0], 10, 0)

    assert shifted.shape == original_shape
    assert shifted.shape == (28, 28)


def test_find_limits_function(notebook_namespace):
    """Test find_limits returns valid bounds."""
    X_train = notebook_namespace['X_train']
    find_limits = notebook_namespace['find_limits']

    top, bottom, left, right = find_limits(X_train[0])

    # Test bounds are valid
    assert 0 <= top <= bottom < 28
    assert 0 <= left <= right < 28

    # Test specific expected values for first image
    assert (top, bottom, left, right) == (5, 24, 4, 23)


def test_crop_image_limits_function(notebook_namespace):
    """Test crop_image_limits reduces or maintains size."""
    X_train = notebook_namespace['X_train']
    crop_image_limits = notebook_namespace['crop_image_limits']

    original = X_train[0]
    cropped = crop_image_limits(original)

    assert cropped.shape[0] <= 28
    assert cropped.shape[1] <= 28
    assert cropped.size <= original.size

    # Test specific expected size for first image
    assert cropped.shape == (20, 20)


def test_augmented_dataset_size(notebook_namespace):
    """Test augmented dataset has expected size."""
    X_train = notebook_namespace['X_train']
    X_train_augmented = notebook_namespace['X_train_augmented']

    # Should be 5x original: original + noisy + binarized + noisy_binarized + shifted
    expected_size = X_train.shape[0] * 5
    assert X_train_augmented.shape == (expected_size, 28, 28)
    assert X_train_augmented.shape == (300000, 28, 28)
