import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 성능 최적화 설정
  
  // Docker 배포를 위한 standalone 모드 (선택사항)
  // output: "standalone",
  
  // 이미지 최적화
  images: {
    formats: ["image/avif", "image/webp"],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    minimumCacheTTL: 60,
  },

  // 압축 활성화
  compress: true,

  // 프로덕션 소스맵 비활성화 (빌드 속도 향상)
  productionBrowserSourceMaps: false,

  // SWC 컴파일러 최적화
  swcMinify: true,

  // 실험적 기능
  experimental: {
    // 서버 액션 활성화
    serverActions: {
      bodySizeLimit: "2mb",
    },
  },

  // 헤더 설정 (캐싱, 보안)
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "X-Frame-Options",
            value: "DENY",
          },
          {
            key: "X-XSS-Protection",
            value: "1; mode=block",
          },
        ],
      },
      {
        source: "/static/(.*)",
        headers: [
          {
            key: "Cache-Control",
            value: "public, max-age=31536000, immutable",
          },
        ],
      },
    ];
  },

  // 웹팩 설정 (청크 최적화)
  webpack: (config, { isServer }) => {
    if (!isServer) {
      // 클라이언트 사이드 청크 최적화
      config.optimization = {
        ...config.optimization,
        splitChunks: {
          chunks: "all",
          cacheGroups: {
            default: false,
            vendors: false,
            // 공통 모듈
            commons: {
              name: "commons",
              chunks: "all",
              minChunks: 2,
              priority: 10,
            },
            // React 관련 라이브러리
            react: {
              name: "react",
              test: /[\\/]node_modules[\\/](react|react-dom|scheduler)[\\/]/,
              priority: 20,
            },
            // UI 라이브러리
            ui: {
              name: "ui",
              test: /[\\/]components[\\/]ui[\\/]/,
              priority: 15,
            },
          },
        },
      };
    }
    return config;
  },
};

export default nextConfig;
