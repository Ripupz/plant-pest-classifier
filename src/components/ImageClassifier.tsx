import { useState, useRef } from 'react';
import { Upload, Loader2, Image as ImageIcon, Sparkles } from 'lucide-react';

interface Prediction {
  className: string;
  probability: number;
}

export function ImageClassifier() {
  const [predicting, setPredicting] = useState(false);
  const [image, setImage] = useState<string | null>(null);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [imageFile, setImageFile] = useState<File | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);

  // ✅ Local backend
  const API_URL = 'http://127.0.0.1:8000';

  const classifyImage = async () => {
    if (!imageFile) return;

    setPredicting(true);

    try {
      const form = new FormData();
      form.append('file', imageFile);

      const resp = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: form,
      });

      if (!resp.ok) {
        const text = await resp.text();
        throw new Error(`Server error: ${resp.status} ${text}`);
      }

      const data = await resp.json();
      console.log('API response:', data);

      /**
       * Expected backend response:
       * {
       *   "prediction": "Jute Aphid",
       *   "confidence": 0.87
       * }
       */
      setPredictions([
        {
          className: data.prediction,
          probability: data.confidence,
        },
      ]);
    } catch (error) {
      console.error('Error classifying image:', error);
    }

    setPredicting(false);
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      setImage(event.target?.result as string);
      setPredictions([]);
      setImageFile(file);
    };
    reader.readAsDataURL(file);
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleReset = () => {
    setImage(null);
    setPredictions([]);
    setImageFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8">
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        className="hidden"
      />

      {!image && (
        <div
          onClick={handleUploadClick}
          className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center cursor-pointer hover:border-emerald-400 hover:bg-emerald-50 transition"
        >
          <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 mb-2">Click to upload a plant pest image</p>
          <p className="text-gray-400">PNG, JPG, JPEG</p>
        </div>
      )}

      {image && (
        <div className="space-y-6">
          <img
            ref={imageRef}
            src={image}
            alt="Uploaded"
            className="w-full rounded-lg"
            onLoad={() => {
              if (!predicting && predictions.length === 0) {
                classifyImage();
              }
            }}
          />

          {predicting && (
            <div className="text-center py-6">
              <Loader2 className="w-8 h-8 animate-spin text-emerald-600 mx-auto mb-2" />
              <p className="text-gray-600">Analyzing image...</p>
            </div>
          )}

          {predictions.length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-emerald-600">
                <Sparkles className="w-5 h-5" />
                <h3 className="font-semibold">Prediction Result</h3>
              </div>

              {predictions.map((p, idx) => (
                <div
                  key={idx}
                  className="bg-emerald-50 rounded-lg p-4"
                >
                  <div className="flex justify-between mb-2">
                    <span className="font-medium">{p.className}</span>
                    <span className="text-emerald-600">
                      {(p.probability * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 h-2 rounded-full">
                    <div
                      className="bg-emerald-500 h-2 rounded-full"
                      style={{ width: `${p.probability * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="flex gap-3">
            <button
              onClick={handleUploadClick}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
            >
              <ImageIcon className="w-5 h-5" />
              Upload New Image
            </button>

            <button
              onClick={handleReset}
              className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              Reset
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
