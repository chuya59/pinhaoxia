from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pinghaoxia",
    version="6.0.0",
    author="Lady W",
    author_email="",
    description="拼好虾 (PingHaoXia) - 多智能体去中心化协作网络",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LadyW/pinghaoxia",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Flask>=2.3.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "prod": [
            "gunicorn>=21.0.0",
            "redis>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pinghaoxia-server=hub_server:main",
        ],
    },
    package_data={
        "pinghaoxia": ["src/scripts/*.py", "src/*.md"],
    },
)