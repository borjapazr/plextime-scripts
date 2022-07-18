from setuptools import find_packages, setup

setup(
    name="plextime-scripts",
    version="1.0.0",
    author="Borja Paz Rodríguez (@borjapazr)",
    author_email="borjapazr@gmail.com",
    url="https://me.marsmachine.space",
    description="Automatic checking in and checking out to Plexus Tech",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.0",
    install_requires=[
        "requests==2.28.1",
        "pycryptodome==3.10.1",
        "schedule==1.1.0",
        "coloredlogs==15.0",
        "colorama==0.4.4",
        "pre-commit==2.18.1",
    ],
    entry_points={
        "console_scripts": [
            "checkin=src.scripts.checkin:main",
            "random-checkin=src.scripts.checkin:random_checkin",
            "checkout=src.scripts.checkout:main",
            "random-checkout=src.scripts.checkout:random_checkout",
            "journal-options=src.scripts.journal_options:main",
        ]
    },
)
