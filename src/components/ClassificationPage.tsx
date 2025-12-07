import { ArrowLeft, Leaf } from 'lucide-react';
import { ImageClassifier } from './ImageClassifier';

interface ClassificationPageProps {
  onNavigate: () => void;
}

export function ClassificationPage({ onNavigate }: ClassificationPageProps) {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-sm border-b border-emerald-200">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Leaf className="w-8 h-8 text-emerald-600" />
              <span className="text-emerald-900">Plant Pest Classifier</span>
            </div>
            <button
              onClick={onNavigate}
              className="flex items-center gap-2 px-6 py-2 bg-white text-emerald-600 border border-emerald-600 rounded-lg hover:bg-emerald-50 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Home
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-emerald-800 mb-4">Plant Pest & Disease Classification</h1>
            <p className="text-gray-600">
              Upload your plant image and let our AI detect and identify pests or diseases
            </p>
          </div>
          <ImageClassifier />
        </div>
      </div>
    </div>
  );
}