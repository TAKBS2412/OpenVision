#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/gpu/gpu.hpp>

class ImageFiltering {
	private:
	cv::gpu::GpuMat inRange(cv::gpu::GpuMat *img, cv::Scalar lower, cv::Scalar higher) {
		cv::gpu::GpuMat shsv[3];
		cv::gpu::GpuMat thresch[3];
		cv::gpu::GpuMat threscl[3];
		cv::gpu::GpuMat thresc[3];
		cv::gpu::GpuMat temp;
		cv::gpu::GpuMat thres;

		//Split HSV 3 channels
		cv::gpu::split(*img, shsv);

		//Threshold HSV channels
		cv::gpu::threshold(shsv[0], thresch[0], lower[0], 255, cv::THRESH_BINARY);
		cv::gpu::threshold(shsv[1], thresch[1], lower[1], 255, cv::THRESH_BINARY);
		cv::gpu::threshold(shsv[2], thresch[2], lower[2], 255, cv::THRESH_BINARY);

		cv::gpu::threshold(shsv[0], threscl[0], higher[0], 255, cv::THRESH_BINARY_INV);
		cv::gpu::threshold(shsv[1], threscl[1], higher[1], 255, cv::THRESH_BINARY_INV);
		cv::gpu::threshold(shsv[2], threscl[2], higher[2], 255, cv::THRESH_BINARY_INV);

		cv::gpu::bitwise_and(thresch[0], threscl[0], thresc[0]);
		cv::gpu::bitwise_and(thresch[1], threscl[1], thresc[1]);
		cv::gpu::bitwise_and(thresch[2], threscl[2], thresc[2]);

		//Bitwise AND the channels
		cv::gpu::bitwise_and(thresc[0], thresc[1],temp);
		cv::gpu::bitwise_and(temp, thresc[2], thres);
		
		*img = thres;
		return thres;
	}
	public:
	cv::Mat& filterImage(cv::Mat &img) {
		int lowerh = 50;
		int lowers = 200;
		int lowerv = 30;
		int higherh = 66;
		int highers = 255;
		int higherv = 255;

		cv::gpu::GpuMat *src = new cv::gpu::GpuMat();
		cv::gpu::GpuMat *dst = new cv::gpu::GpuMat();

		src->upload(img);

		cv::gpu::cvtColor(*src, *dst, CV_BGR2HSV);
		inRange(dst, cv::Scalar(lowerh, lowers, lowerv), cv::Scalar(higherh, highers, higherv));
		dst->download(img);
		
		delete src;
		delete dst;
	
		return img;
	}
};
