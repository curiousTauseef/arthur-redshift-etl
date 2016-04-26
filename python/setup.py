import os
import os.path
from setuptools import setup, find_packages


setup(
    name="redshift-etl",
    version="0.3.3",
    packages=find_packages(),
    package_data={'etl': ["config/*"]},
    scripts=[
        "scripts/initial_setup.py",
        "scripts/create_user.py",
        "scripts/dump_to_s3.py",
        "scripts/split_csv.py",
        "scripts/load_to_redshift.py",
        "scripts/copy_to_s3.py",
        "scripts/update_from_ctas.py",
        "scripts/update_views.py",
        "baseline/modified_rows.py"
    ]
)
