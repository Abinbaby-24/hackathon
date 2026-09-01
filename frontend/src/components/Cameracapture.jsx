import { useEffect, useRef, useState } from "react";

function CameraCapture({ onCapture, onCancel }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const streamRef = useRef(null);

  const [cameraOn, setCameraOn] = useState(false);
  const [error, setError] = useState("");

  // ==========================================
  // START CAMERA
  // ==========================================

  const startCamera = async () => {
    try {
      setError("");

      if (!navigator.mediaDevices?.getUserMedia) {
        setError(
          "Camera access is not supported by this browser."
        );
        return;
      }

      // Stop any existing stream first
      if (streamRef.current) {
        streamRef.current
          .getTracks()
          .forEach((track) => track.stop());
      }

      const mediaStream =
        await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });

      streamRef.current = mediaStream;

      setCameraOn(true);

      // Wait for video element to render
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;

          videoRef.current
            .play()
            .catch((err) => {
              console.error(
                "Video play error:",
                err
              );
            });
        }
      }, 100);

    } catch (err) {
      console.error(
        "Camera error:",
        err
      );

      if (err.name === "NotAllowedError") {
        setError(
          "Camera permission was denied. Please allow camera access."
        );
      } else if (err.name === "NotFoundError") {
        setError(
          "No camera was found on this device."
        );
      } else if (err.name === "NotReadableError") {
        setError(
          "The camera is already being used by another application."
        );
      } else {
        setError(
          "Unable to access the camera."
        );
      }
    }
  };


  // ==========================================
  // AUTOMATICALLY START CAMERA
  // ==========================================

  useEffect(() => {
    startCamera();

    return () => {
      if (streamRef.current) {
        streamRef.current
          .getTracks()
          .forEach((track) => track.stop());

        streamRef.current = null;
      }
    };
  }, []);


  // ==========================================
  // STOP CAMERA
  // ==========================================

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current
        .getTracks()
        .forEach((track) => track.stop());

      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setCameraOn(false);
  };


  // ==========================================
  // CAPTURE PHOTO
  // ==========================================

  const captureImage = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (!video || !canvas) {
      setError("Camera is not ready.");
      return;
    }

    if (
      video.videoWidth === 0 ||
      video.videoHeight === 0
    ) {
      setError(
        "Camera is not ready yet. Please wait."
      );
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context =
      canvas.getContext("2d");

    context.drawImage(
      video,
      0,
      0,
      canvas.width,
      canvas.height
    );

    canvas.toBlob(
      (blob) => {
        if (!blob) {
          setError(
            "Unable to capture image."
          );
          return;
        }

        const file = new File(
          [blob],
          `package-${Date.now()}.jpg`,
          {
            type: "image/jpeg",
          }
        );

        // Send image to Upload.jsx
        onCapture(file);

        // Stop camera
        stopCamera();
      },
      "image/jpeg",
      0.95
    );
  };


  // ==========================================
  // CANCEL
  // ==========================================

  const handleCancel = () => {
    stopCamera();

    if (onCancel) {
      onCancel();
    }
  };


  // ==========================================
  // UI
  // ==========================================

  return (
    <div className="camera-container">

      {cameraOn ? (

        <div className="camera-preview">

          <video
            ref={videoRef}
            autoPlay
            muted
            playsInline
            className="camera-video"
          />

          <div className="camera-actions">

            <button
              type="button"
              className="primary-btn"
              onClick={captureImage}
            >
              📸 Capture Photo
            </button>

            <button
              type="button"
              className="secondary-btn"
              onClick={handleCancel}
            >
              Cancel
            </button>

          </div>

        </div>

      ) : (

        !error && (
          <div className="camera-loading">
            <p>
              Starting camera...
            </p>
          </div>
        )

      )}

      {error && (
        <div>
          <p className="error-message">
            {error}
          </p>

          <button
            type="button"
            className="camera-btn"
            onClick={startCamera}
          >
            🔄 Try Again
          </button>
        </div>
      )}

      <canvas
        ref={canvasRef}
        style={{
          display: "none"
        }}
      />

    </div>
  );
}

export default CameraCapture;