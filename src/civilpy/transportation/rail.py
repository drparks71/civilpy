from dataclasses import dataclass
from typing import Optional, Tuple
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import Session


@dataclass
class RailSection:
    weight: Optional[int] = None
    rail_id: Optional[str] = None
    database_url: str = "sqlite:///civilpy.db"  # Replace with your DB connection string

    def __post_init__(self):
        # Create a database connection
        engine = create_engine(self.database_url)
        metadata = MetaData()
        rail_sections = Table('rail_sections', metadata, autoload_with=engine)

        with Session(engine) as session:
            # Determine if rail_id is provided or weight needs to be matched
            if self.rail_id:
                query = select(rail_sections).where(rail_sections.c.id == self.rail_id)
                result = session.execute(query).fetchone()
                if result:
                    self.display_result(result)
                else:
                    raise ValueError(f"No rail section found with ID: {self.rail_id}")
            elif self.weight:
                query = select(rail_sections).where(rail_sections.c.weight == self.weight)
                results = session.execute(query).fetchall()
                if len(results) == 1:
                    self.display_result(results[0])
                elif len(results) > 1:
                    raise ValueError(f"Multiple rail sections found with weight: {self.weight}")
                else:
                    raise ValueError(f"No rail sections found with weight: {self.weight}")
            else:
                raise ValueError("Either rail_id or weight must be provided.")

    def display_result(self, result: Tuple):
        """Helper method to display the found rail section"""
        print(f"Found rail section: ID={result['id']}, Weight={result['weight']}")
