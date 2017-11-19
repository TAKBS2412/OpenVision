#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/gpu/gpu.hpp>

class ImageFiltering {
	public:
	cv::Mat& filterImage(cv::Mat &img) {
		cv::gpu::GpuMat *src = new cv::gpu::GpuMat();
		cv::gpu::GpuMat *dst = new cv::gpu::GpuMat();

		src->upload(img);

		cv::gpu::cvtColor(*src, *dst, CV_BGR2HSV);

		dst->download(img);

		int lowerh = 50;
		int lowers = 200;
		int lowerv = 30;
		int higherh = 66;
		int highers = 255;
		int higherv = 255;

		cv::inRange(img, cv::Scalar(lowerh, lowers, lowerv), cv::Scalar(higherh, highers, higherv), img);
		
		delete src;
		delete dst;
	
		return img;
	}
};
