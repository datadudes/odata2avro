from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='cornet',
    version='0.1rc1',
    author='Marcel Krcah, Daan Debie',
    author_email='marcel.krcah@gmail.com, debie.daan@gmail.com',
    description='Convert OData to Avro',
    license='MIT',
    keywords='opendata avro hadoop',
    url='https://github.com/datadudes/odata2avro',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        # 'console_scripts': ['tbd=tbd.main:cli']
    },
    install_requires=requirements,
    classifiers=[
        # 'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: Utilities',
    ]
)