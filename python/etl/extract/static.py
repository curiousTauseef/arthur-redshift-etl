import logging
import os.path
from typing import Dict, List

from etl.config.dw import DataWarehouseSchema
from etl.extract.extractor import Extractor
from etl.relation import RelationDescription
from etl.thyme import Thyme


class StaticExtractor(Extractor):

    """
    Enable using files in S3 as an upstream data source.
    """
    # TODO Describe expected file paths, existence of "_SUCCESS" file

    def __init__(self, schemas: Dict[str, DataWarehouseSchema], descriptions: List[RelationDescription],
                 keep_going: bool, dry_run: bool) -> None:
        # For static sources, we go straight to failure when the success file does not exist
        super().__init__("static", schemas, descriptions, keep_going, needs_to_wait=False, dry_run=dry_run)
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def current_location(source: DataWarehouseSchema, description: RelationDescription):
        rendered_template = Thyme.render_template(source.s3_path_template, {"prefix": description.prefix})
        return os.path.join(rendered_template, description.csv_path_name)

    @staticmethod
    def source_info(source: DataWarehouseSchema, description: RelationDescription):
        return {'name': source.name,
                'bucket_name': source.s3_bucket,
                'object_prefix': StaticExtractor.current_location(source, description)}

    def extract_table(self, source: DataWarehouseSchema, description: RelationDescription):
        """
        Render the S3 path template for a given source to check for data files before writing
        out a manifest file
        """
        prefix = self.current_location(source, description)
        bucket = source.s3_bucket
        self.write_manifest_file(description, bucket, prefix)