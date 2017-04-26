from distutils.core import setup

setup(
    name='tbtbot',
    version='0.1dev',
    author='Sehrob Ibrohimov',
    packages=['tbtbot', 'tbtbot.tests'],
    license='License.txt',
    description='Telegram bot',
    long_description=open('README.md').read(),
    install_requires=[
        "envparse >= 0.2.0",
        "tornado==4.4.2",
    ],
    entry_points={
        'console_scripts':
            ['tbtboter = tbtbot.tbtboter.cli:main',]
    },
)

