/** @type {import('next').NextConfig} */

const nextConfig = {
  allowedDevOrigins: [
    "192.168.29.9",
    "localhost"
  ],

  // keep cache local to project
  distDir: ".next",

  turbopack: {}
}

module.exports = nextConfig