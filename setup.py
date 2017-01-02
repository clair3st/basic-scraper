"""Setup simple scraper module."""


from setuptools import setup

setup(
    name="Scraper",
    description="Build a simple scraper for food inspection",
    version=0.1,
    author=["Claire Gatenby"],
    author_email="clairejgatenby@gmail.com",
    licencse="MIT",
    # package_dir={'': 'src'},
    py_modules=["scraper"],
    install_requires=['html5lib'],
    extras_require={
        "test": ["pytest", "pytest-cov", "tox"]
    }
)
