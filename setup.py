from setuptools import setup


setup(
    name="redshift-etl",
    version="0.19.0",
    author="Harry's Data Engineering and Contributors",
    description="ETL code to ferry data from PostgreSQL databases to Redshift cluster",
    license="MIT",
    keywords="redshift postgresql etl extract transform load",
    url="https://github.com/harrystech/harrys-redshift-etl",
    package_dir={"": "python"},
    packages=["etl", "etl.config"],
    package_data={"etl": ["config/*"]},
    scripts=["python/scripts/submit_arthur.sh"],
    entry_points={
        # NB The script must end in ".py" so that spark submit accepts it as a Python script.
        "console_scripts": ["arthur.py=etl.commands:run_arg_as_command"]
    }
)
