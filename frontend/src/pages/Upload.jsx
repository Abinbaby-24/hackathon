import { useState } from "react";
import { useNavigate } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";
import ImageUploader from "../components/ImageUploader";
import CameraCapture from "../components/Cameracapture";
import api from "../services/api";

function Upload() {
  const navigate = useNavigate();

  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);

  const [cameraOpen, setCameraOpen] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // ==========================================
  // IMAGE UPLOAD FROM COMPUTER
  // ==========================================

  const handleImageChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    if (!file.type.startsWith("image/")) {
      setError("Please select a valid image.");
      return;
    }

    setError("");

    setSelectedImage(file);

    setPreview(URL.createObjectURL(file));

    // Make sure camera is closed
    setCameraOpen(false);
  };


  // ==========================================
  // OPEN CAMERA
  // ==========================================

  const openCamera = () => {
    setError("");
    setCameraOpen(true);
  };


  // ==========================================
  // CAMERA CAPTURE
  // ==========================================

  const handleCameraCapture = (file) => {
    if (!file) return;

    setError("");

    setSelectedImage(file);

    setPreview(URL.createObjectURL(file));

    // Close camera after taking photo
    setCameraOpen(false);
  };


  // ==========================================
  // CANCEL CAMERA
  // ==========================================

  const handleCameraCancel = () => {
    setCameraOpen(false);
    setError("");
  };


  // ==========================================
  // REMOVE IMAGE
  // ==========================================

  const removeImage = () => {
    setSelectedImage(null);
    setPreview(null);
    setError("");
    setCameraOpen(false);
  };


  // ==========================================
  // RETAKE IMAGE
  // ==========================================

  const handleRetake = () => {
    // Remove old image
    setSelectedImage(null);
    setPreview(null);
    setError("");

    // Automatically open camera
    setCameraOpen(true);
  };


  // ==========================================
  // SCAN IMAGE
  // ==========================================

  const handleScan = async () => {
    if (!selectedImage) {
      setError(
        "Please upload or capture a package image first."
      );

      return;
    }

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();

      // IMPORTANT:
      // This must match your Flask backend.
      formData.append("image", selectedImage);

      const response = await api.post(
        "/scan",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log(
        "Scan response:",
        response.data
      );

      // Save inspection result
      localStorage.setItem(
        "inspectionResult",
        JSON.stringify(response.data)
      );

      // Navigate to result page
      navigate("/result");

    } catch (err) {
      console.error(
        "Scan error:",
        err
      );

      setError(
        err.response?.data?.message ||
        "Scanning failed. Please try again."
      );

    } finally {
      setLoading(false);
    }
  };


  // ==========================================
  // PAGE
  // ==========================================

  return (
    <MainLayout>

      {/* PAGE HEADER */}

      <div className="page-header">

        <div>

          <h1>
            New Inspection
          </h1>

          <p>
            Upload or capture a package image
            for compliance analysis
          </p>

        </div>

      </div>


      <div className="upload-container">


        {/* ====================================
            CAMERA OPEN
        ==================================== */}

        {cameraOpen ? (

          <div className="camera-section">

            <div className="camera-box">

              <h3>
                Capture Package Image
              </h3>

              <p className="camera-instruction">
                Position the package clearly
                inside the camera.
              </p>

              <CameraCapture
                onCapture={handleCameraCapture}
                onCancel={handleCameraCancel}
              />

            </div>

          </div>


        /* ====================================
           IMAGE SELECTED
        ==================================== */

        ) : selectedImage ? (

          <div className="selected-image-container">

            <h3>
              Package Image
            </h3>

            <img
              src={preview}
              alt="Selected package"
              className="selected-package-image"
            />


            {/* IMAGE ACTIONS */}

            <div className="image-actions">

              <button
                type="button"
                className="retake-btn"
                onClick={handleRetake}
              >
                🔄 Retake
              </button>

              <button
                type="button"
                className="remove-btn"
                onClick={removeImage}
              >
                🗑 Remove Image
              </button>

            </div>

          </div>


        /* ====================================
           NO IMAGE
        ==================================== */

        ) : (

          <div>

            {/* NORMAL IMAGE UPLOAD */}

            <ImageUploader
              selectedImage={selectedImage}
              preview={preview}
              onImageChange={handleImageChange}
              onRemove={removeImage}
            />


            {/* OR */}

            <div className="camera-section">

              <p className="camera-or">
                OR
              </p>

              <h3>
                Capture Package Using Camera
              </h3>

              <button
                type="button"
                className="camera-btn"
                onClick={openCamera}
              >
                📷 Open Camera
              </button>

            </div>

          </div>
        )}


        {/* ====================================
            ERROR
        ==================================== */}

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}


        {/* ====================================
            LOADING
        ==================================== */}

        {loading ? (

          <div className="loading-box">

            <div className="spinner"></div>

            <h2>
              Inspecting Package...
            </h2>

            <p>
              Please wait while AI analyzes
              the package.
            </p>

            <div className="processing-steps">

              <p>
                ✓ Uploading Image
              </p>

              <p>
                ⏳ Processing Image
              </p>

              <p>
                ⏳ Extracting Text
              </p>

              <p>
                ⏳ Analyzing Product Information
              </p>

              <p>
                ⏳ Checking Compliance
              </p>

            </div>

          </div>

        ) : (

          /* ==================================
             SCAN BUTTON
          ================================== */

          <button
            type="button"
            className="scan-btn"
            onClick={handleScan}
            disabled={!selectedImage}
          >
            🔍 Scan Package
          </button>

        )}

      </div>

    </MainLayout>
  );
}

export default Upload;