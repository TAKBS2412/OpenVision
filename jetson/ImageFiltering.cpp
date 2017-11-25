#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/gpu/gpu.hpp>

class ImageFiltering {
	public:
	cv::Mat& filterImage(cv::Mat &img) {
		clock_t t;
		t = clock();
		cv::gpu::GpuMat *src = new cv::gpu::GpuMat();
		cv::gpu::GpuMat *dst = new cv::gpu::GpuMat();
		t = clock() - t;

		std::cout << "ImageFiltering (gpuinit) - Time elapsed (s): " << ((float)t)/CLOCKS_PER_SEC << "\n";
	
		t = clock();
		src->upload(img); //THIS TAKES A WHILE THE FIRST TIME
		t = clock() - t;
	
		std::cout << "ImageFiltering (imgupload) - Time elapsed (s): " << ((float)t)/CLOCKS_PER_SEC << "\n";

		cv::gpu::cvtColor(*src, *dst, CV_BGR2HSV);

		dst->download(img);
			
		int lowerh = 50;
		int lowers = 200;
		int lowerv = 30;
		int higherh = 66;
		int highers = 255;
		int higherv = 255;
		t = clock();
		cv::inRange(img, cv::Scalar(lowerh, lowers, lowerv), cv::Scalar(higherh, highers, higherv), img);
		t = clock() - t;
		std::cout << "ImageFiltering (inRange) - Time elapsed (s): " << ((float)t)/CLOCKS_PER_SEC << "\n";


		delete src;
		delete dst;
	
		return img;
	}
};
