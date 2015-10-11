from setuptools import setup


setup(
    name='nosedive',
    version='0.10',
    url='https://github.com/mattboyer/',
    description=('Hurr Durr'),
    author='Matt Boyer',
    author_email='mboyer@sdf.org',
    license='BSD',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
    ],
    keywords='nosetests',
    packages=['NoseDive'],
    install_requires=['nose'],
    entry_points = {
        'nose.plugins.0.10': [ 'krunt = NoseDive.depth:DepthPlugin' ] },
)
