DROP DATABASE IF EXISTS `elearning_python_db`;
CREATE DATABASE `elearning_python_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `elearning_python_db`;

SET NAMES utf8mb4;
SET TIME_ZONE='+00:00';
SET FOREIGN_KEY_CHECKS=0;
SET UNIQUE_CHECKS=0;
SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO';

CREATE TABLE `NguoiDung` (
  `tai_khoan` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mat_khau` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ho_ten` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `so_dt` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ma_loai_nguoi_dung` enum('HV','GV','GVU') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'HV',
  `ma_nhom` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'GP01',
  `avatar` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bio` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `updated_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `unlocked_courses` varchar(2000) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`tai_khoan`),
  UNIQUE KEY `uk_nguoidung_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `NguoiDung` VALUES
('admin01','$2b$10$m4RUZqVhFSUTFjSC.IlAZuiCJeO3NzLkSquRgkjxdJjDNEIPOFUu2','Nguyễn Minh Quân','admin01@elearning.vn','0901234567','GV','GP01',NULL,'Quản trị viên hệ thống và phụ trách chương trình đào tạo công nghệ thông tin.','2026-07-31 15:15:05.007','2026-08-01 20:50:17.916',1,''),
('admin02','$2b$10$tNMEdq5zeQVHSQXhvYcsYepCrcAI0uwjOXxh8ZrpvxUQVKuekKJ8W','Trần Thu Hà','admin02@elearning.vn','0902345678','GVU','GP01',NULL,'Phụ trách giáo vụ và kiểm định chất lượng học tập trực tuyến.','2026-07-31 15:15:05.007','2026-08-01 20:50:39.968',1,''),
('giangvien01','$2b$10$CuFnC/H48mxd2gV8zOkObeH1mRT/fTfLBZV1pig4ah2VMiO1DtCh6','Lê Hoàng Nam','nam.le@elearning.vn','0912345678','GV','GP01',NULL,'Giảng viên lập trình Web Full-Stack và kiến trúc hệ thống phân tán.','2026-07-31 15:15:05.007','2026-07-31 15:15:05.007',1,''),
('giangvien02','$2b$10$CuFnC/H48mxd2gV8zOkObeH1mRT/fTfLBZV1pig4ah2VMiO1DtCh6','Phạm Thanh Thảo','thao.pham@elearning.vn','0913456789','GV','GP01',NULL,'Tiến sĩ Khoa học Máy tính, giảng viên chuyên ngành Khoa học Dữ liệu và Trí tuệ nhân tạo.','2026-07-31 15:15:05.007','2026-07-31 15:15:05.007',1,''),
('student01','$2b$10$CuFnC/H48mxd2gV8zOkObeH1mRT/fTfLBZV1pig4ah2VMiO1DtCh6','Võ Quốc Bảo','bao.vo@sinhvien.edu.vn','0987654321','HV','GP01',NULL,'Sinh viên năm cuối chuyên ngành Kỹ thuật Phần mềm.','2026-07-31 15:15:05.007','2026-07-31 15:15:05.007',1,'FE_REACT'),
('student02','$2b$10$CuFnC/H48mxd2gV8zOkObeH1mRT/fTfLBZV1pig4ah2VMiO1DtCh6','Đặng Ngọc Ánh','anh.dang@sinhvien.edu.vn','0988888888','HV','GP01',NULL,'Học viên định hướng phát triển ứng dụng Web và Điện toán đám mây.','2026-07-31 15:15:05.007','2026-07-31 15:15:05.007',1,''),
('trinhgiang','$2b$10$tqzIJgRFyFh6n41oZCtnFOCGfWM4PHJXQBGhhixvI7nDq0AN67DK2','Trịnh Xuân Giang','trinhgiang.dev16@gmail.com','0847557925','HV','GP01',NULL,'Học viên chuyên ngành Công nghệ thông tin.','2026-08-01 18:03:12.630','2026-08-02 07:22:32.492',1,'UIUX_FIGMA_MASTER,QA_AUTOMATION_SELENIUM,DO_DOCKER_K8S');

CREATE TABLE `DanhMucKhoaHoc` (
  `ma_danh_muc` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ten_danh_muc` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `icon` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`ma_danh_muc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `DanhMucKhoaHoc` VALUES
('BACK_END','Lập trình Back-End & Microservices','server','2026-07-31 15:15:05.033'),
('DATA_AI','Khoa học Dữ liệu & Trí tuệ Nhân tạo (AI)','cpu','2026-07-31 15:15:05.033'),
('DATABASE','Hệ quản trị Cơ sở Dữ liệu','database','2026-07-31 15:15:05.033'),
('DEVOPS_CLOUD','Triển khai Hệ thống DevOps & Cloud','cloud','2026-07-31 15:15:05.033'),
('FRONT_END','Lập trình Giao diện Web Front-End','code','2026-07-31 15:15:05.033'),
('FULL_STACK','Lập trình Web Full-Stack','layers','2026-07-31 15:15:05.033'),
('MOBILE','Lập trình Ứng dụng Di động','smartphone','2026-07-31 15:15:05.033'),
('SECURITY','An toàn Thông tin & Bảo mật Mạng','shield','2026-07-31 15:15:05.033'),
('TESTING_QA','Kiểm thử Phần mềm & Tự động hóa QA','check-circle','2026-07-31 15:15:05.033'),
('UI_UX_DESIGN','Thiết kế Giao diện UI/UX','figma','2026-07-31 15:15:05.033');

CREATE TABLE `KhoaHoc` (
  `ma_khoa_hoc` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ten_khoa_hoc` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bi_anh` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mo_ta` longtext COLLATE utf8mb4_unicode_ci,
  `luot_xem` int NOT NULL DEFAULT '0',
  `danh_gia` double NOT NULL DEFAULT '5',
  `hinh_anh` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ma_nhom` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'GP01',
  `ngay_tao` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `cap_do` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'CoBan',
  `thoi_luong_gio` int NOT NULL DEFAULT '0',
  `trang_thai` tinyint(1) NOT NULL DEFAULT '1',
  `ma_danh_muc` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tai_khoan_tao` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`ma_khoa_hoc`),
  KEY `idx_khoahoc_danhmuc` (`ma_danh_muc`),
  KEY `idx_khoahoc_nguoitao` (`tai_khoan_tao`),
  CONSTRAINT `fk_khoahoc_danhmuc` FOREIGN KEY (`ma_danh_muc`) REFERENCES `DanhMucKhoaHoc` (`ma_danh_muc`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_khoahoc_nguoitao` FOREIGN KEY (`tai_khoan_tao`) REFERENCES `NguoiDung` (`tai_khoan`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `KhoaHoc` VALUES
('AI_MACHINE_LEARNING','Học máy Ứng dụng và Mô hình Thống kê (Machine Learning)','AI_MACHINE_LEARNING','Nắm vững các thuật toán Machine Learning cốt lõi với Python và Scikit-Learn: Hồi quy tuyến tính, Cây quyết định, Random Forest và Phân cụm dữ liệu.',2037,5,'https://images.unsplash.com/photo-1507146426996-ef05306b995a?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.825','TrungCap',90,1,'DATA_AI','giangvien02'),
('AI_PYTHON_DATA','Phân tích Dữ liệu (Data Science) với Python','AI_PYTHON_DATA','Trở thành chuyên viên phân tích dữ liệu (Data Analyst): Làm chủ ngôn ngữ Python, thư viện NumPy, Pandas DataFrame, trực quan hóa dữ liệu và thống kê.',2171,5,'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.787','CoBan',70,1,'DATA_AI','giangvien02'),
('BE_DOTNET','Xây dựng Web API với C# .NET 8 và Entity Framework Core','BE_DOTNET','Phát triển hệ thống RESTful Web API tốc độ cao trên nền tảng .NET 8: Minimal APIs, EF Core Code-First, Repository Pattern và quản trị SQL Server.',2483,5,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2L8TeulhXxsWs7d3TQ3F-qyYHCdnYRxBn092AehwTMw&s=10','GP01','2026-07-31 15:15:05.587','TrungCap',85,1,'BACK_END','giangvien01'),
('BE_GOLANG','Lập trình Back-End Hiệu năng cao với ngôn ngữ Go (Golang)','BE_GOLANG','Làm chủ ngôn ngữ lập trình hệ thống hiện đại Golang: Xử lý đồng thời với Goroutines, Channels, Gin Framework, GORM và dịch vụ gRPC.',2316,5,'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.534','TrungCap',70,1,'BACK_END','giangvien01'),
('BE_NESTJS','Kiến trúc Microservices Doanh nghiệp với NestJS và TypeScript','BE_NESTJS','Thiết kế dịch vụ Back-End chuẩn doanh nghiệp với NestJS: Dependency Injection, Modules, Controllers, Guards, Interceptors và tích hợp TypeORM.',2033,5,'https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.441','TrungCap',80,1,'BACK_END','giangvien01'),
('BE_NODEJS','Lập trình Back-End với Node.js, ExpressJS và Hệ CSDL','BE_NODEJS','Xây dựng hệ thống RESTful API hoàn chỉnh: Cơ chế Event Loop, Express Middleware, xác thực bảo mật JWT và phân quyền người dùng.',1724,5,'https://images.unsplash.com/photo-1627398242454-45a1465c2479?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.396','CoBan',75,1,'BACK_END','giangvien01'),
('BE_SPRING','Lập trình Java Spring Boot 3 và Spring Cloud Microservices','BE_SPRING','Kỹ thuật phần mềm Back-End bằng Java: Spring MVC, Spring Data JPA, bảo mật Spring Security OAuth2, Eureka Discovery và API Gateway.',2735,5,'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.478','NangCao',120,1,'BACK_END','giangvien01'),
('DB_SQL_MASTER','Làm chủ Cơ sở Dữ liệu Quan hệ: MySQL và PostgreSQL','DB_SQL_MASTER','Thiết kế và tối ưu hóa cơ sở dữ liệu SQL: Truy vấn JOIN phức tạp, CTE Subqueries, đánh chỉ mục B-Tree Index, Transaction và Stored Procedure.',1248,5,'https://images.unsplash.com/photo-1544383835-bda2bc66a55d?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:06.049','CoBan',75,1,'DATABASE','giangvien01'),
('DO_AWS_SOLUTIONS','Kiến trúc sư Giải pháp Đám mây AWS (Solutions Architect)','DO_AWS_SOLUTIONS','Quản trị hạ tầng điện toán đám mây AWS: Máy chủ ảo EC2, lưu trữ S3, cơ sở dữ liệu RDS, mạng VPC, phân quyền IAM và cân bằng tải.',675,5,'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.900','TrungCap',110,1,'DEVOPS_CLOUD','giangvien01'),
('DO_DOCKER_K8S','Thực hành Đóng gói và Điều phối Hệ thống với Docker & Kubernetes','DO_DOCKER_K8S','Đóng gói container và tự động hóa triển khai ứng dụng: Tối ưu hóa Dockerfile đa tầng, quản lý Kubernetes Pods, Deployments và Ingress.',2502,5,'https://images.unsplash.com/photo-1605745341112-85968b19335b?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.863','CoBan',75,1,'DEVOPS_CLOUD','giangvien01'),
('FE_ANGULAR','Phát triển Ứng dụng Web Doanh nghiệp với Angular 17','FE_ANGULAR','Xây dựng hệ thống Front-End quy mô lớn sử dụng Angular Signals, xử lý bất đồng bộ RxJS, Dependency Injection và quản lý trạng thái NgRx.',992,5,'https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.319','TrungCap',85,1,'FRONT_END','giangvien01'),
('FE_HTML_CSS','Nền tảng Thiết kế Web Hiện đại với HTML5, CSS3 và Flexbox/Grid','FE_HTML_CSS','Kiến thức nền tảng vững chắc cho lập trình viên giao diện Web: Thẻ ngữ nghĩa HTML5, bố cục CSS Flexbox, Grid 2D và thiết kế đáp ứng đa thiết bị.',524,5,'https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.355','CoBan',48,1,'FRONT_END','giangvien01'),
('FE_NEXTJS','Lập trình Web Nâng cao với Next.js 14 và React Server Components','FE_NEXTJS','Phát triển ứng dụng ReactJS chuẩn doanh nghiệp với Next.js 14: React Server Components, Server Actions, tối ưu hóa SEO và cơ chế lưu đệm.',2547,5,'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.268','NangCao',90,1,'FRONT_END','giangvien01'),
('FE_REACT','Lập trình Front-End Chuyên sâu với ReactJS 18 và Redux Toolkit','FE_REACT','Khóa học toàn diện về ReactJS 18: Cơ chế Virtual DOM, xây dựng Custom Hooks, quản lý trạng thái bằng Redux Toolkit và tối ưu hiệu năng.',1296,5,'https://images.unsplash.com/photo-1633356122544-f134324a6cee?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.056','TrungCap',72,1,'FRONT_END','giangvien01'),
('FE_VUE','Phát triển Giao diện Web với Vue.js 3 và Nuxt 3 Framework','FE_VUE','Làm chủ Vue 3 Composition API, quản lý trạng thái Pinia, định tuyến Vue Router và kết xuất phía máy chủ với Nuxt 3.',1609,5,'https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.188','CoBan',60,1,'FRONT_END','giangvien01'),
('FS_MERN','Lập trình Web Toàn diện với MERN Stack (MongoDB, Express, React, Node.js)','FS_MERN','Xây dựng ứng dụng Web hoàn chỉnh từ đầu đến cuối: Cơ sở dữ liệu MongoDB, REST API với Express, giao diện React SPA và triển khai thực tế.',682,5,'https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.628','CoBan',100,1,'FULL_STACK','giangvien01'),
('FS_NEXT_PRISMA','Xây dựng Ứng dụng Full-Stack Hiện đại với Next.js 14 và PostgreSQL','FS_NEXT_PRISMA','Kỹ thuật lập trình Full-Stack thế hệ mới: Tích hợp Next.js App Router, truy vấn cơ sở dữ liệu an toàn kiểu dữ liệu và xác thực người dùng.',2817,5,'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.666','NangCao',110,1,'FULL_STACK','giangvien01'),
('MOB_FLUTTER','Lập trình Ứng dụng Di động Đa nền tảng với Flutter và Dart','MOB_FLUTTER','Phát triển ứng dụng iOS và Android từ một mã nguồn duy nhất: Ngôn ngữ Dart, thiết kế Widget tùy chỉnh, kiến trúc BLoC và tích hợp Firebase.',944,5,'https://images.unsplash.com/photo-1551650975-87deedd944c3?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.746','CoBan',85,1,'MOBILE','giangvien01'),
('MOB_REACT_NATIVE','Phát triển Ứng dụng Di động iOS & Android với React Native','MOB_REACT_NATIVE','Xây dựng ứng dụng di động thực tế bằng React Native và Expo: Quản lý trạng thái với Redux Toolkit, điều hướng màn hình và tích hợp API thiết bị.',588,5,'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.706','CoBan',80,1,'MOBILE','giangvien01'),
('QA_AUTOMATION_SELENIUM','Kiểm thử Phần mềm Tự động với Selenium WebDriver và Java','QA_AUTOMATION_SELENIUM','Trở thành kỹ sư kiểm thử tự động chuyên nghiệp: Thiết kế kịch bản kiểm thử với Selenium WebDriver, TestNG Framework và mô hình Page Object Model.',1456,5,'https://d3hi6wehcrq5by.cloudfront.net/itnavi-blog/2020/04/Tester-l%C3%A0-g%C3%AC-4.jpg','GP01','2026-07-31 15:15:05.973','CoBan',80,1,'TESTING_QA','giangvien01'),
('SEC_WEB_PENTEST','Kiểm thử Xâm nhập Ứng dụng Web và Bảo mật theo chuẩn OWASP Top 10','SEC_WEB_PENTEST','Thực hành đánh giá an toàn thông tin ứng dụng Web: Phát hiện và phòng chống lỗ hổng SQL Injection, XSS, CSRF, SSRF cùng công cụ Burp Suite.',1349,5,'https://images.unsplash.com/photo-1563986768609-322da13575f3?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:05.937','TrungCap',85,1,'SECURITY','giangvien02'),
('UIUX_FIGMA_MASTER','Thiết kế Giao diện và Trải nghiệm Người dùng Chuyên nghiệp với Figma','UIUX_FIGMA_MASTER','Làm chủ quy trình thiết kế sản phẩm số trên Figma: Xây dựng Design System, bố cục tự động Auto-Layout, tạo nguyên mẫu tương tác và bàn giao thiết kế.',1838,5,'https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?q=80&w=800&auto=format&fit=crop','GP01','2026-07-31 15:15:06.013','CoBan',70,1,'UI_UX_DESIGN','giangvien02');

CREATE TABLE `ChuongHoc` (
  `ma_chuong` int NOT NULL AUTO_INCREMENT,
  `ma_khoa_hoc` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ten_chuong` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `thu_tu` int NOT NULL DEFAULT '1',
  `created_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`ma_chuong`),
  KEY `idx_chuonghoc_khoahoc` (`ma_khoa_hoc`),
  CONSTRAINT `fk_chuonghoc_khoahoc` FOREIGN KEY (`ma_khoa_hoc`) REFERENCES `KhoaHoc` (`ma_khoa_hoc`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=308 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `ChuongHoc` VALUES
(283,'FE_REACT','Chương 1: Nền tảng React 18 và Kiến trúc JSX',1,'2026-07-31 15:15:05.067'),
(284,'FE_REACT','Chương 2: Lập trình chuyên sâu với React Hooks',2,'2026-07-31 15:15:05.110'),
(285,'FE_REACT','Chương 3: Quản lý trạng thái toàn cục với Redux Toolkit',3,'2026-07-31 15:15:05.151'),
(286,'FE_VUE','Chương 1: Cốt lõi Vue 3 Composition API',1,'2026-07-31 15:15:05.202'),
(287,'FE_VUE','Chương 2: Quản lý trạng thái ứng dụng với Pinia',2,'2026-07-31 15:15:05.240'),
(288,'FE_NEXTJS','Chương 1: Kiến trúc Next.js 14 App Router và React Server Components',1,'2026-07-31 15:15:05.279'),
(289,'FE_ANGULAR','Chương 1: Kiến trúc Standalone Components trong Angular',1,'2026-07-31 15:15:05.328'),
(290,'FE_HTML_CSS','Chương 1: Thẻ ngữ nghĩa HTML5 và Bố cục CSS',1,'2026-07-31 15:15:05.365'),
(291,'BE_NODEJS','Chương 1: Khởi tạo Máy chủ Express và Định tuyến Phân tầng',1,'2026-07-31 15:15:05.404'),
(292,'BE_NESTJS','Chương 1: Kiến trúc Module và Dependency Injection trong NestJS',1,'2026-07-31 15:15:05.450'),
(293,'BE_SPRING','Chương 1: Truy xuất Dữ liệu với Spring Data JPA',1,'2026-07-31 15:15:05.487'),
(294,'BE_GOLANG','Chương 1: Lập trình Đồng thời trong Golang',1,'2026-07-31 15:15:05.548'),
(295,'BE_DOTNET','Chương 1: Phát triển .NET 8 Web API và EF Core',1,'2026-07-31 15:15:05.597'),
(296,'FS_MERN','Chương 1: Kiến trúc Kết nối Toàn diện MERN Stack',1,'2026-07-31 15:15:05.638'),
(297,'FS_NEXT_PRISMA','Chương 1: Phát triển Ứng dụng Full-Stack phía Máy chủ',1,'2026-07-31 15:15:05.676'),
(298,'MOB_REACT_NATIVE','Chương 1: Nền tảng React Native và Quy trình Expo',1,'2026-07-31 15:15:05.717'),
(299,'MOB_FLUTTER','Chương 1: Cơ bản về Flutter Framework và Dart',1,'2026-07-31 15:15:05.758'),
(300,'AI_PYTHON_DATA','Chương 1: Thư viện Phân tích Dữ liệu Cốt lõi trong Python',1,'2026-07-31 15:15:05.797'),
(301,'AI_MACHINE_LEARNING','Chương 1: Thuật toán Học có Giám sát và Không Giám sát',1,'2026-07-31 15:15:05.834'),
(302,'DO_DOCKER_K8S','Chương 1: Đóng gói Container với Docker và Điều phối Kubernetes',1,'2026-07-31 15:15:05.875'),
(303,'DO_AWS_SOLUTIONS','Chương 1: Dịch vụ Tính toán và Lưu trữ Đám mây AWS',1,'2026-07-31 15:15:05.909'),
(304,'SEC_WEB_PENTEST','Chương 1: Phân tích Lỗ hổng Bảo mật Web OWASP',1,'2026-07-31 15:15:05.947'),
(305,'QA_AUTOMATION_SELENIUM','Chương 1: Thiết kế Khung Kiểm thử Tự động Selenium',1,'2026-07-31 15:15:05.983'),
(306,'UIUX_FIGMA_MASTER','Chương 1: Xây dựng Hệ thống Thiết kế trên Figma',1,'2026-07-31 15:15:06.023'),
(307,'DB_SQL_MASTER','Chương 1: Tối ưu hóa Hiệu năng Truy vấn Cơ sở Dữ liệu Quan hệ',1,'2026-07-31 15:15:06.058');

CREATE TABLE `BaiHoc` (
  `ma_bai_hoc` int NOT NULL AUTO_INCREMENT,
  `ma_chuong` int NOT NULL,
  `ten_bai_hoc` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `loai_bai_hoc` enum('VIDEO','ARTICLE','DOCUMENT') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'VIDEO',
  `url_video` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `noi_dung_text` longtext COLLATE utf8mb4_unicode_ci,
  `thoi_luong_giay` int NOT NULL DEFAULT '0',
  `thu_tu` int NOT NULL DEFAULT '1',
  `is_preview` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`ma_bai_hoc`),
  KEY `idx_baihoc_chuong` (`ma_chuong`),
  CONSTRAINT `fk_baihoc_chuong` FOREIGN KEY (`ma_chuong`) REFERENCES `ChuongHoc` (`ma_chuong`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=902 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `BaiHoc` VALUES
(846,283,'Tổng quan về React 18 và cơ chế Virtual DOM','VIDEO','THL1OPnV208','Tài liệu bài giảng chi tiết về kiến trúc React 18 và cơ chế đồng bộ Virtual DOM. Học viên thực hành khởi tạo dự án mẫu.',600,1,1,'2026-07-31 15:15:05.079'),
(847,283,'Cú pháp JSX và tư duy chia nhỏ Component','VIDEO','dQw4w9WgXcQ','Hướng dẫn cách viết cú pháp JSX chuẩn xác, truyền dữ liệu và tổ chức cây giao diện theo mô hình Component.',600,2,0,'2026-07-31 15:15:05.092'),
(848,283,'Quản lý Props, State và vòng đời sự kiện','VIDEO','dGcsHMXbSOA','Phân biệt dữ liệu bất biến Props và trạng thái nội tại State, cách xử lý sự kiện tương tác của người dùng.',600,3,0,'2026-07-31 15:15:05.102'),
(849,284,'Sử dụng thành thạo useState và useEffect','VIDEO','N3AkSS5hXMA','Nắm vững hai Hook quan trọng nhất trong React để quản lý trạng thái và xử lý các tác vụ bất đồng bộ gọi API.',600,1,1,'2026-07-31 15:15:05.123'),
(850,284,'Tối ưu hóa hiệu năng với useMemo và useCallback','VIDEO','dQw4w9WgXcQ','Kỹ thuật ngăn chặn việc kết xuất lại không cần thiết và đo lường hiệu năng ứng dụng bằng công cụ React Profiler.',600,2,0,'2026-07-31 15:15:05.132'),
(851,284,'Xây dựng Custom Hooks tái sử dụng logic','VIDEO','dQw4w9WgXcQ','Phương pháp đóng gói logic nghiệp vụ vào các Custom Hooks giúp mã nguồn ngắn gọn và dễ bảo trì.',600,3,0,'2026-07-31 15:15:05.141'),
(852,285,'Kiến trúc Redux và thiết lập Store toàn cục','VIDEO','dGcsHMXbSOA','Giới thiệu luồng dữ liệu một chiều trong Redux Toolkit và cách cấu hình Store cho dự án thực tế.',600,1,1,'2026-07-31 15:15:05.161'),
(853,285,'Xử lý bất đồng bộ với createAsyncThunk và Middleware','VIDEO','O6P86uwfdz0','Tích hợp gọi REST API và quản lý các trạng thái đang tải, thành công hoặc thất bại trong Redux.',600,2,0,'2026-07-31 15:15:05.170'),
(854,285,'Chiến lược lưu đệm dữ liệu với RTK Query','VIDEO','N3AkSS5hXMA','Tối ưu hóa truy vấn dữ liệu từ máy chủ và tự động đồng bộ giao diện bằng công cụ RTK Query.',600,3,0,'2026-07-31 15:15:05.179'),
(855,286,'Khởi tạo dự án Vue 3 với công cụ Vite','VIDEO','gUz4H2HkHSw','Thiết lập môi trường phát triển tốc độ cao cho ứng dụng Vue 3 cùng cấu trúc thư mục chuẩn.',600,1,1,'2026-07-31 15:15:05.212'),
(856,286,'Hệ thống phản ứng dữ liệu: ref và reactive','VIDEO','dGcsHMXbSOA','Hiểu sâu cơ chế Reactivity trong Vue 3 và khi nào nên sử dụng ref hoặc reactive.',600,2,0,'2026-07-31 15:15:05.222'),
(857,286,'Thuộc tính tính toán Computed và theo dõi Watchers','VIDEO','Ke90Tje7VS0','Xử lý dữ liệu dẫn xuất tự động và lắng nghe sự thay đổi trạng thái trong ứng dụng Vue.',600,3,0,'2026-07-31 15:15:05.230'),
(858,287,'Thiết lập Pinia Store và định nghĩa Actions','VIDEO','dQw4w9WgXcQ','Quản lý trạng thái tập trung cho ứng dụng Vue 3 bằng thư viện chính thức Pinia.',600,1,1,'2026-07-31 15:15:05.249'),
(859,287,'Lưu trữ trạng thái bền vững và kiến trúc Plugin','VIDEO','dQw4w9WgXcQ','Đồng bộ dữ liệu Pinia với bộ nhớ trình duyệt và mở rộng tính năng qua Plugin.',600,2,0,'2026-07-31 15:15:05.258'),
(860,288,'Phân biệt kiến trúc Server Component và Client Component','VIDEO','dQw4w9WgXcQ','Hiểu rõ cơ chế kết xuất trên máy chủ của Next.js 14 và cách kết hợp với React Client Component.',600,1,1,'2026-07-31 15:15:05.289'),
(861,288,'Định tuyến dựa trên thư mục và Parallel Routes','VIDEO','O6P86uwfdz0','Tổ chức bố cục trang nâng cao, xử lý trạng thái tải trang và bắt lỗi trong Next.js App Router.',600,2,0,'2026-07-31 15:15:05.300'),
(862,288,'Xử lý biểu mẫu trực tiếp với Server Actions','VIDEO','dQw4w9WgXcQ','Thực hiện cập nhật dữ liệu an toàn từ giao diện React lên máy chủ mà không cần viết tầng API rời rạc.',600,3,0,'2026-07-31 15:15:05.309'),
(863,289,'Cú pháp điều khiển luồng mới trong Angular 17','VIDEO','dGcsHMXbSOA','Áp dụng cú pháp khối lệnh mới giúp template Angular trực quan và tăng tốc độ biên dịch.',600,1,1,'2026-07-31 15:15:05.336'),
(864,289,'Kết hợp luồng dữ liệu RxJS Observables và Signals','VIDEO','N3AkSS5hXMA','Quản lý luồng sự kiện thời gian thực và đồng bộ trạng thái giao diện mượt mà.',600,2,0,'2026-07-31 15:15:05.346'),
(865,290,'Xây dựng cấu trúc thẻ HTML5 chuẩn SEO','VIDEO','dGcsHMXbSOA','Sử dụng đúng các thẻ ngữ nghĩa giúp công cụ tìm kiếm lập chỉ mục hiệu quả và hỗ trợ khả năng tiếp cận.',600,1,1,'2026-07-31 15:15:05.377'),
(866,290,'Mô hình hộp CSS Box Model và bố cục Grid 2 chiều','VIDEO','O6P86uwfdz0','Thực hành dàn trang phức tạp thích ứng trên cả màn hình máy tính, máy tính bảng và điện thoại.',600,2,0,'2026-07-31 15:15:05.387'),
(867,291,'Cơ chế vòng lặp sự kiện bất đồng bộ Event Loop trong Node.js','VIDEO','dGcsHMXbSOA','Phân tích cách Node.js xử lý hàng ngàn kết nối đồng thời trên một luồng đơn.',600,1,1,'2026-07-31 15:15:05.415'),
(868,291,'Thiết kế kiến trúc Controller và Service chuẩn RESTful','VIDEO','Ke90Tje7VS0','Tổ chức mã nguồn phân lớp rõ ràng giúp ứng dụng Express dễ dàng mở rộng.',600,2,0,'2026-07-31 15:15:05.424'),
(869,291,'Xây dựng Middleware xử lý lỗi và xác thực tập trung','VIDEO','N3AkSS5hXMA','Kiểm soát toàn bộ ngoại lệ của hệ thống và bảo vệ các tuyến API bằng JWT.',600,3,0,'2026-07-31 15:15:05.432'),
(870,292,'Cơ chế Dependency Injection Container trong NestJS','VIDEO','Ke90Tje7VS0','Áp dụng nguyên lý đảo ngược phụ thuộc để giảm sự gắn kết chặt giữa các thành phần.',600,1,1,'2026-07-31 15:15:05.459'),
(871,292,'Bảo vệ API với Guards và phân quyền theo vai trò RBAC','VIDEO','Ke90Tje7VS0','Triển khai cơ chế kiểm tra quyền hạn chi tiết cho từng đối tượng người dùng.',600,2,0,'2026-07-31 15:15:05.469'),
(872,293,'Ánh xạ quan hệ thực thể JPA và tối ưu hóa truy vấn','VIDEO','O6P86uwfdz0','Giải quyết bài toán truy vấn N+1 và quản lý kết nối cơ sở dữ liệu hiệu quả trong Spring Boot.',600,1,1,'2026-07-31 15:15:05.498'),
(873,293,'Cấu hình chuỗi bộ lọc bảo mật Spring Security','VIDEO','2_l9rP6ZtH4','Tích hợp xác thực người dùng bằng Token và phân quyền truy cập tài nguyên.',600,2,0,'2026-07-31 15:15:05.511'),
(874,294,'Xử lý đồng thời với Goroutines và Channels','VIDEO','O6P86uwfdz0','Khai thác sức mạnh đa luồng siêu nhẹ của Golang bằng Goroutines và giao tiếp an toàn qua Channels.',600,1,1,'2026-07-31 15:15:05.566'),
(875,294,'Xây dựng dịch vụ HTTP với Gin Framework và GORM','VIDEO','dGcsHMXbSOA','Phát triển REST API tốc độ phản hồi cực nhanh kết nối cơ sở dữ liệu quan hệ.',600,2,0,'2026-07-31 15:15:05.578'),
(876,295,'So sánh kiến trúc Minimal API và Controller trong .NET 8','VIDEO','Ke90Tje7VS0','Lựa chọn mô hình thiết kế điểm cuối API phù hợp với quy mô dự án doanh nghiệp.',600,1,1,'2026-07-31 15:15:05.608'),
(877,295,'Tối ưu hóa hiệu năng truy vấn LINQ và Entity Framework','VIDEO','dQw4w9WgXcQ','Sử dụng AsNoTracking, biên dịch truy vấn và phân trang dữ liệu lớn trên SQL Server.',600,2,0,'2026-07-31 15:15:05.618'),
(878,296,'Phát triển tầng dịch vụ REST API với Express và MongoDB','VIDEO','N3AkSS5hXMA','Thiết kế lược đồ tài liệu Mongoose và xây dựng các API nghiệp vụ hoàn chỉnh.',600,1,1,'2026-07-31 15:15:05.647'),
(879,296,'Tích hợp giao diện React với Redux Toolkit và Axios','VIDEO','6ThXcHsSgO4','Kết nối giao diện người dùng với máy chủ Back-End và quản lý phiên đăng nhập.',600,2,0,'2026-07-31 15:15:05.656'),
(880,297,'Thao tác dữ liệu trực tiếp với Next.js Server Actions','VIDEO','FMnlyi60avU','Xây dựng luồng thêm, sửa, xóa dữ liệu tốc độ cao kèm kiểm tra hợp lệ đầu vào.',600,1,1,'2026-07-31 15:15:05.685'),
(881,297,'Thiết kế lược đồ cơ sở dữ liệu tối ưu và tạo chỉ mục','VIDEO','dQw4w9WgXcQ','Quản lý phiên bản cơ sở dữ liệu và tối ưu hóa các truy vấn kết nối nhiều bảng.',600,2,0,'2026-07-31 15:15:05.696'),
(882,298,'Thiết kế bố cục màn hình di động với Flexbox','VIDEO','dGcsHMXbSOA','Xây dựng giao diện thích ứng trên nhiều kích thước màn hình iOS và Android.',600,1,1,'2026-07-31 15:15:05.726'),
(883,298,'Điều hướng màn hình với React Navigation Stack và Tabs','VIDEO','dGcsHMXbSOA','Tổ chức luồng di chuyển giữa các màn hình và truyền tham số trong ứng dụng di động.',600,2,0,'2026-07-31 15:15:05.736'),
(884,299,'Ngữ pháp ngôn ngữ Dart và lập trình hướng đối tượng','VIDEO','dQw4w9WgXcQ','Làm quen với hệ thống kiểu dữ liệu, bất đồng bộ Future/Stream trong ngôn ngữ Dart.',600,1,1,'2026-07-31 15:15:05.767'),
(885,299,'Quản lý trạng thái ứng dụng Flutter theo kiến trúc BLoC','VIDEO','GLSG_Wh_YWc','Tách biệt hoàn toàn giao diện Widget và tầng xử lý nghiệp vụ trong dự án Flutter.',600,2,0,'2026-07-31 15:15:05.777'),
(886,300,'Tính toán ma trận và vector hóa dữ liệu với thư viện NumPy','VIDEO','N3AkSS5hXMA','Xử lý mảng đa chiều tốc độ cao làm nền tảng cho phân tích dữ liệu và học máy bằng Python.',600,1,1,'2026-07-31 15:15:05.807'),
(887,300,'Làm sạch và tổng hợp dữ liệu bảng với thư viện Pandas','VIDEO','dGcsHMXbSOA','Thực hành đọc dữ liệu, xử lý giá trị khuyết thiếu, gộp nhóm và thống kê trên DataFrame.',600,2,0,'2026-07-31 15:15:05.816'),
(888,301,'Xây dựng mô hình Hồi quy và Phân loại trong Machine Learning','VIDEO','O6P86uwfdz0','Huấn luyện các thuật toán học có giám sát để dự đoán số liệu và phân lớp đối tượng.',600,1,1,'2026-07-31 15:15:05.845'),
(889,301,'Đánh giá chất lượng mô hình và trích xuất đặc trưng dữ liệu','VIDEO','Ke90Tje7VS0','Sử dụng kiểm định chéo Cross-Validation, ma trận nhầm lẫn và chuẩn hóa đặc trưng đầu vào.',600,2,0,'2026-07-31 15:15:05.854'),
(890,302,'Tối ưu hóa dung lượng ảnh контейner với Multi-Stage Dockerfile','VIDEO','3c-iQQXJVJs','Kỹ thuật viết Dockerfile đa tầng giúp giảm kích thước image và tăng tính bảo mật khi vận hành.',600,1,1,'2026-07-31 15:15:05.883'),
(891,302,'Triển khai và quản lý dịch vụ trên cụm Kubernetes','VIDEO','N3AkSS5hXMA','Cấu hình tệp manifest cho Deployment, Service, ConfigMap và tự động mở rộng quy mô Pod.',600,2,0,'2026-07-31 15:15:05.892'),
(892,303,'Thiết lập cụm máy chủ tự động co giãn EC2 Auto Scaling','VIDEO','Ke90Tje7VS0','Đảm bảo tính sẵn sàng cao cho ứng dụng Web trên hạ tầng đám mây Amazon Web Services.',600,1,1,'2026-07-31 15:15:05.917'),
(893,303,'Quản lý lưu trữ đối tượng S3 và phân quyền bảo mật IAM','VIDEO','2_l9rP6ZtH4','Lưu trữ tài nguyên tĩnh an toàn và thiết lập chính sách truy cập tối thiểu.',600,2,0,'2026-07-31 15:15:05.926'),
(894,304,'Kỹ thuật chặn bắt và phân tích gói tin HTTP với Burp Suite','VIDEO','N3AkSS5hXMA','Thiết lập môi trường kiểm thử bảo mật và kiểm tra luồng dữ liệu giữa trình duyệt và máy chủ.',600,1,1,'2026-07-31 15:15:05.955'),
(895,304,'Khai thác và phòng chống lỗ hổng SQL Injection thực tế','VIDEO','HXV3zeQKqGY','Hiểu nguyên nhân gây ra lỗi tiêm mã SQL và cách khắc phục triệt để bằng truy vấn tham số hóa.',600,2,0,'2026-07-31 15:15:05.964'),
(896,305,'Thiết kế kiến trúc kiểm thử theo mẫu Page Object Model','VIDEO','N3AkSS5hXMA','Tách biệt mã định vị phần tử giao diện và kịch bản kiểm thử giúp dễ dàng bảo trì.',600,1,1,'2026-07-31 15:15:05.992'),
(897,305,'Thực thi bộ kiểm thử tự động TestNG và xuất báo cáo','VIDEO','Ke90Tje7VS0','Tự động hóa quy trình chạy kiểm thử hồi quy và tổng hợp báo cáo kết quả trực quan.',600,2,0,'2026-07-31 15:15:06.001'),
(898,306,'Quy tắc thiết kế bố cục tự động co giãn với Auto Layout','VIDEO','Ke90Tje7VS0','Xây dựng các thành phần giao diện linh hoạt tự động điều chỉnh kích thước theo nội dung.',600,1,1,'2026-07-31 15:15:06.031'),
(899,306,'Tạo nguyên mẫu tương tác và quản lý biến thể Component','VIDEO','O6P86uwfdz0','Mô phỏng luồng trải nghiệm người dùng chân thực trước khi chuyển giao cho đội ngũ lập trình.',600,2,0,'2026-07-31 15:15:06.041'),
(900,307,'Phân tích kế hoạch thực thi truy vấn JOIN và đánh chỉ mục Index','VIDEO','dGcsHMXbSOA','Sử dụng lệnh EXPLAIN để tìm điểm nghẽn và tối ưu hóa tốc độ truy vấn trên bảng dữ liệu lớn.',600,1,1,'2026-07-31 15:15:06.067'),
(901,307,'Quản lý giao dịch ACID và cơ chế khóa dữ liệu trong SQL','VIDEO','Ke90Tje7VS0','Đảm bảo tính toàn vẹn dữ liệu trong các nghiệp vụ tài chính và xử lý tranh chấp đồng thời.',600,2,0,'2026-07-31 15:15:06.075');

CREATE TABLE `BaiTap` (
  `ma_bai_tap` int NOT NULL AUTO_INCREMENT,
  `ma_bai_hoc` int NOT NULL,
  `tieu_de` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `de_bai_mo_ta` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `han_nop` datetime(3) DEFAULT NULL,
  `created_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`ma_bai_tap`),
  KEY `idx_baitap_baihoc` (`ma_bai_hoc`),
  CONSTRAINT `fk_baitap_baihoc` FOREIGN KEY (`ma_bai_hoc`) REFERENCES `BaiHoc` (`ma_bai_hoc`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=264 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `BaiTap` VALUES
(259,846,'Bài tập thực hành: Xây dựng giao diện Quản lý Khóa học bằng React 18','Thiết kế và lập trình trang danh sách khóa học có bộ lọc tìm kiếm theo danh mục. Nộp đường dẫn mã nguồn GitHub của bạn.',NULL,'2026-07-31 15:15:06.085'),
(261,900,'Bài tập thực hành: Tối ưu hóa câu truy vấn SQL trên CSDL Đào tạo','Viết các câu truy vấn thống kê học viên và thiết lập chỉ mục B-Tree cho bảng Tiến độ bài học.','2026-12-31 23:59:59.000','2026-08-01 22:24:30.303'),
(263,901,'Bài tập thực hành: Xây dựng Stored Procedure xử lý Ghi danh Khóa học','Áp dụng Transaction để đảm bảo tính toàn vẹn dữ liệu khi học viên đăng ký khóa học mới.','2026-12-31 23:59:59.000','2026-08-02 09:39:59.127');

CREATE TABLE `GhiChuBaiHoc` (
  `ma_ghi_chu` int NOT NULL AUTO_INCREMENT,
  `tai_khoan` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ma_bai_hoc` int NOT NULL,
  `timestamp` int NOT NULL DEFAULT '0',
  `noi_dung` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`ma_ghi_chu`),
  KEY `idx_ghichu_taikhoan` (`tai_khoan`),
  KEY `idx_ghichu_baihoc` (`ma_bai_hoc`),
  CONSTRAINT `fk_ghichu_baihoc` FOREIGN KEY (`ma_bai_hoc`) REFERENCES `BaiHoc` (`ma_bai_hoc`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_ghichu_taikhoan` FOREIGN KEY (`tai_khoan`) REFERENCES `NguoiDung` (`tai_khoan`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `GhiChuBaiHoc` VALUES
(3,'student01',846,45,'Cần sử dụng React.memo để tránh việc render lại các phần tử danh sách lớn không cần thiết.','2026-08-01 21:56:07.583'),
(4,'student01',846,155,'Hàm dọn dẹp (cleanup function) trong useEffect giúp hủy bộ đếm thời gian và tránh rò rỉ bộ nhớ.','2026-08-01 21:56:07.612'),
(5,'student01',846,310,'Tách logic gọi API ra Custom Hook giúp phần giao diện Component gọn gàng và dễ kiểm thử hơn.','2026-08-01 21:56:07.650'),
(6,'trinhgiang',898,60,'Thiết lập Auto Layout giúp khung giao diện tự động co giãn khi thay đổi độ dài văn bản tiếng Việt.','2026-08-02 07:09:54.222');

CREATE TABLE `NopBaiTap` (
  `ma_luot_nop` int NOT NULL AUTO_INCREMENT,
  `ma_bai_tap` int NOT NULL,
  `tai_khoan` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `link_nop_bai` varchar(1000) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ghi_chu_student` text COLLATE utf8mb4_unicode_ci,
  `diem_so` double DEFAULT NULL,
  `nhan_xet_gv` text COLLATE utf8mb4_unicode_ci,
  `trang_thai` enum('CHUA_CHAM','DA_CHAM') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'CHUA_CHAM',
  `ngay_nop` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `updated_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`ma_luot_nop`),
  UNIQUE KEY `uk_nopbaitap_baitap_taikhoan` (`ma_bai_tap`,`tai_khoan`),
  KEY `idx_nopbaitap_taikhoan` (`tai_khoan`),
  CONSTRAINT `fk_nopbaitap_baitap` FOREIGN KEY (`ma_bai_tap`) REFERENCES `BaiTap` (`ma_bai_tap`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_nopbaitap_taikhoan` FOREIGN KEY (`tai_khoan`) REFERENCES `NguoiDung` (`tai_khoan`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `NopBaiTap` VALUES
(5,259,'student01','https://github.com/student01/react-course-dashboard','Em đã hoàn thành đầy đủ các chức năng tìm kiếm và phân trang theo yêu cầu đề bài ạ.',NULL,NULL,'CHUA_CHAM','2026-07-31 15:15:06.100','2026-07-31 15:15:06.100'),
(6,261,'trinhgiang','https://github.com/trinhgiang/sql-query-optimization','Em nộp bài tập tối ưu hóa truy vấn và đánh chỉ mục cho bảng dữ liệu.',90,'Câu truy vấn viết tối ưu, sử dụng chỉ mục hợp lý giúp giảm đáng kể thời gian tìm kiếm.','DA_CHAM','2026-08-02 06:54:21.195','2026-08-02 06:54:47.633');

CREATE TABLE `TienDoBaiHoc` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tai_khoan` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ma_bai_hoc` int NOT NULL,
  `da_hoan_thanh` tinyint(1) NOT NULL DEFAULT '0',
  `thoi_gian_xem` int NOT NULL DEFAULT '0',
  `watched_intervals` json DEFAULT NULL,
  `actual_watched_seconds` int NOT NULL DEFAULT '0',
  `last_ping_at` datetime(3) DEFAULT NULL,
  `updated_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_tiendo_taikhoan_baihoc` (`tai_khoan`,`ma_bai_hoc`),
  KEY `idx_tiendo_baihoc` (`ma_bai_hoc`),
  CONSTRAINT `fk_tiendo_baihoc` FOREIGN KEY (`ma_bai_hoc`) REFERENCES `BaiHoc` (`ma_bai_hoc`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_tiendo_taikhoan` FOREIGN KEY (`tai_khoan`) REFERENCES `NguoiDung` (`tai_khoan`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `TienDoBaiHoc` (`id`, `tai_khoan`, `ma_bai_hoc`, `da_hoan_thanh`, `thoi_gian_xem`, `watched_intervals`, `actual_watched_seconds`, `last_ping_at`, `updated_at`) VALUES
(2,'student01',846,0,0,'[]',0,'2026-07-31 15:15:06.149','2026-07-31 15:15:06.149'),
(5,'trinhgiang',898,1,600,'[[0, 600]]',600,'2026-08-02 06:51:27.161','2026-08-02 06:51:27.161'),
(6,'trinhgiang',899,1,600,'[[0, 600]]',600,'2026-08-02 06:55:24.073','2026-08-02 06:55:24.073'),
(8,'trinhgiang',896,1,600,'[[0, 600]]',600,'2026-08-02 07:08:43.556','2026-08-02 07:08:43.556'),
(9,'trinhgiang',897,1,600,'[[0, 600]]',600,'2026-08-02 07:10:03.371','2026-08-02 07:10:03.371'),
(10,'trinhgiang',890,1,600,'[[0, 600]]',600,'2026-08-02 07:22:35.724','2026-08-02 07:22:35.724');

CREATE TABLE `GhiDanhKhoaHoc` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tai_khoan` VARCHAR(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ma_khoa_hoc` VARCHAR(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ngay_ghi_danh` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `trang_thai` TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ghidanh_taikhoan_khoahoc` (`tai_khoan`, `ma_khoa_hoc`),
  KEY `idx_ghidanh_khoahoc` (`ma_khoa_hoc`),
  CONSTRAINT `fk_ghidanh_khoahoc` FOREIGN KEY (`ma_khoa_hoc`) REFERENCES `KhoaHoc` (`ma_khoa_hoc`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_ghidanh_taikhoan` FOREIGN KEY (`tai_khoan`) REFERENCES `NguoiDung` (`tai_khoan`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `GhiDanhKhoaHoc` (`tai_khoan`, `ma_khoa_hoc`) VALUES
('student01', 'FE_REACT'),
('trinhgiang', 'UIUX_FIGMA_MASTER'),
('trinhgiang', 'QA_AUTOMATION_SELENIUM'),
('trinhgiang', 'DO_DOCKER_K8S');

SET FOREIGN_KEY_CHECKS=1;
SET UNIQUE_CHECKS=1;
