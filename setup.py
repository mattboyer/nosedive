from setuptools import setup
import version


setup(
    name='nosedive',
    version=version.get_git_version(),
    url='https://github.com/mattboyer/',
    description=('Nosedive is a stack depth tracer for Nose'),
    author='Matt Boyer',
    author_email='mboyer@sdf.org',
    license='BSD',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
    ],
    keywords='nosetests',
    packages=['NoseDive'],
    install_requires=['nose'],
    entry_points={
        'nose.plugins.0.10': ['nosedive = NoseDive.depth:DepthPlugin']
    },
)
