import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  compiler: {
    ...(process.env.ENVIRONMENT === "production" ? {
      reactRemoveProperties: { properties: ["data-testid"] },
      removeConsole: { exclude: ["error", "warn"] },
    } : {}),
  },
};

export default nextConfig;