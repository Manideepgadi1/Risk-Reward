from setuptools import setup, find_packages

setup(
    name="risk-reward-api",
    version="1.0.0",
    description="Risk-Reward Analysis API for Indian Stock Indices",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        'flask>=2.0.0',
        'pandas>=1.3.0',
        'numpy>=1.21.0',
    ],
    include_package_data=True,
    package_data={
        'riskapp': ['data.csv', 'static/*', 'templates/*'],
    },
    python_requires='>=3.7',
)
