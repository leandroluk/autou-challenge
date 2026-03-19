import type { NextConfig } from "next";

const { ENVIRONMENT = "development" } = process.env;

const nextConfig: NextConfig = {
  compiler: {
    ...(ENVIRONMENT === "production" ? {
      reactRemoveProperties: { properties: ["data-testid"] }
    } : {}),
  }
};

export default nextConfig;
