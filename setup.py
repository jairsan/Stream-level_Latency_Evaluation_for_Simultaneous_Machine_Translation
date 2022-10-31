from setuptools import setup, find_packages
setup(
    name='streaming_latency_tk',
    version='0.1.0',
    packages=find_packages(exclude=["emnlp2021", "tests"]),
    entry_points={
        'console_scripts': [
            'stream_latency = streaming_latency_tk.__main__:main_cli',
            'stream_resegment = streaming_latency_tk.resegment:main_cli',
        ]
    },
    install_requires=[
        'python_Levenshtein==0.12.2',
        'numpy'
    ],
    url='https://github.com/jairsan/Stream-level_Latency_Evaluation_for_Simultaneous_Machine_Translation',
    license='Apache License 2.0',
    author='Javier Iranzo-Sanchez',
    description='Streaming latency evaluation for simultaneous machine translation'
)
