'use client'

import { ArrowRight, Leaf, ImageIcon, BarChart3, Zap } from 'lucide-react';

interface HomePageProps {
  onNavigate: () => void;
}

export function HomePage({ onNavigate }: HomePageProps) {
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
              className="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
            >
              Get Started
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 bg-emerald-100 text-emerald-700 px-4 py-2 rounded-full mb-6">
              <Zap className="w-4 h-4" />
              <span>Powered by AI Technology</span>
            </div>
            <h1 className="text-emerald-800 mb-6">
              Plant Pest Image Classification System
            </h1>
            <p className="text-gray-600 max-w-2xl mx-auto mb-8">
              Advanced AI-powered image classification for plant pest and disease detection. Upload your plant images and get instant, accurate predictions to identify pests and diseases affecting your crops.
            </p>
            <button
              onClick={onNavigate}
              className="inline-flex items-center gap-2 px-8 py-4 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
            >
              Start Classifying
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-8 mb-16">
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="w-12 h-12 bg-emerald-100 rounded-lg flex items-center justify-center mb-4">
                <ImageIcon className="w-6 h-6 text-emerald-600" />
              </div>
              <h3 className="text-gray-800 mb-2">Easy Upload</h3>
              <p className="text-gray-600">
                Simply drag and drop or click to upload your PES images for instant analysis
              </p>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="w-12 h-12 bg-emerald-100 rounded-lg flex items-center justify-center mb-4">
                <Zap className="w-6 h-6 text-emerald-600" />
              </div>
              <h3 className="text-gray-800 mb-2">Fast Processing</h3>
              <p className="text-gray-600">
                Get results in seconds with our optimized AI model running in your browser
              </p>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="w-12 h-12 bg-emerald-100 rounded-lg flex items-center justify-center mb-4">
                <BarChart3 className="w-6 h-6 text-emerald-600" />
              </div>
              <h3 className="text-gray-800 mb-2">Detailed Results</h3>
              <p className="text-gray-600">
                View confidence scores and multiple predictions for accurate pest and disease identification
              </p>
            </div>
          </div>

          {/* Profile Section */}
          <div className="bg-white rounded-2xl p-8 shadow-xl">
            <h2 className="text-emerald-800 mb-6">About This Project</h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-gray-800 mb-3">System Profile</h3>
                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-emerald-500 rounded-full mt-2"></div>
                    <div>
                      <p className="text-gray-700">Model Type</p>
                      <p className="text-gray-600">Deep Learning Neural Network for Plant Health</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-emerald-500 rounded-full mt-2"></div>
                    <div>
                      <p className="text-gray-700">Processing</p>
                      <p className="text-gray-600">Real-time Browser-based AI</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-emerald-500 rounded-full mt-2"></div>
                    <div>
                      <p className="text-gray-700">Accuracy</p>
                      <p className="text-gray-600">High-confidence pest and disease predictions</p>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-gray-800 mb-3">Key Features</h3>
                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-emerald-500 rounded-full mt-2"></div>
                    <div>
                      <p className="text-gray-600">
                        No server uploads - all processing happens locally in your browser
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-emerald-500 rounded-full mt-2"></div>
                    <div>
                      <p className="text-gray-600">
                        Support for multiple image formats (PNG, JPG, GIF)
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-emerald-500 rounded-full mt-2"></div>
                    <div>
                      <p className="text-gray-600">
                        Instant results with detailed confidence metrics
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-8 pt-8 border-t border-gray-200">
              <div className="text-center">
                <p className="text-gray-600 mb-4">
                  Ready to identify plant pests and diseases?
                </p>
                <button
                  onClick={onNavigate}
                  className="inline-flex items-center gap-2 px-8 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
                >
                  Try Classification Now
                  <ArrowRight className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}