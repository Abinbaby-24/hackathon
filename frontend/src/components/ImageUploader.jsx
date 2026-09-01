function ImageUploader({
  selectedImage,
  preview,
  onImageChange,
  onRemove,
}) {
  return (
    <div className="upload-box">

      {!preview ? (
        <>

          <div className="upload-icon">
            📷
          </div>

          <h3>Upload Package Image</h3>

          <p>
            Upload JPG, JPEG, or PNG image
          </p>

          <label className="upload-btn">

            Choose Image

            <input
              type="file"
              accept="image/png,image/jpeg,image/jpg"
              hidden
              onChange={onImageChange}
            />

          </label>

        </>
      ) : (
        <>

          <img
            src={preview}
            alt="Package preview"
            className="image-preview"
          />

          <p className="file-name">
            {selectedImage?.name}
          </p>

          <button
            className="secondary-btn"
            onClick={onRemove}
          >
            Remove Image
          </button>

        </>
      )}

    </div>
  );
}

export default ImageUploader;