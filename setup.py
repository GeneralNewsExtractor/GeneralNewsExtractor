from setuptools import setup, find_packages

with open('pypi_desc.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='gne',
    packages=find_packages(exclude=[]),
    install_requires=['lxml', 'numpy', 'pyyaml'],
    version='0.1.5',
    description='General extractor of news pages.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Kingname',
    author_email='contact@kingname.info',
    url='https://github.com/kingname/GeneralNewsExtractor',
    keywords=['python', 'webcrawler', 'webspider'],
    python_requires='>=3.6',
    license='MIT',
    classifiers=[
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
    ]
)
