"""
F.R.I.D.A.Y. Repository Map (AST Indexer).
Generates an Aider-style compressed map of the entire codebase for LLM context.
"""

import os
import ast
from pathlib import Path
from typing import List
from friday_engine.logger import logger

class RepoMapper:
    """
    Parses Python ASTs to extract classes, functions, and docstrings,
    creating a highly dense semantic map of the codebase.
    """
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)

    def _extract_ast_signatures(self, file_path: Path) -> List[str]:
        signatures = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    signatures.append(f"class {node.name}:")
                elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    signatures.append(f"  def {node.name}({', '.join(args)}):")
                    
        except SyntaxError:
            pass
        except Exception as e:
            logger.warning(f"RepoMapper could not parse {file_path}: {e}")
            
        return signatures

    def generate_map(self, exclude_dirs: List[str] = None) -> str:
        """Scan the repository and return a compressed AST map."""
        if exclude_dirs is None:
            exclude_dirs = [".git", "__pycache__", ".venv", "node_modules", "data", "logs"]
            
        repo_map = "=== REPOSITORY MAP ===\n"
        
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith(".py"):
                    full_path = Path(root) / file
                    rel_path = full_path.relative_to(self.root_dir)
                    
                    sigs = self._extract_ast_signatures(full_path)
                    if sigs:
                        repo_map += f"\nFile: {rel_path}\n"
                        repo_map += "\n".join(sigs) + "\n"
                        
        return repo_map
