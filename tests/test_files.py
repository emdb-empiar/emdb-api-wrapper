"""Unit tests for EMDB file models."""
from pathlib import Path

import pytest
import responses

from emdb.models.files import BaseFile, FigureFile


class DummyFile(BaseFile):
    """Concrete file model for testing BaseFile behavior."""

    @property
    def source_path(self) -> str:
        return "https://example.org/test-file.dat"


class TestBaseFileDownload:
    """Tests for BaseFile.download."""

    @responses.activate
    def test_download_appends_safe_filename_to_directory(self, tmp_path):
        """Test downloading to a directory appends the file's basename."""
        responses.add(
            responses.GET,
            "https://example.org/test-file.dat",
            body=b"file content",
            status=200,
        )
        file = DummyFile(filename="test-file.dat")

        file.download(str(tmp_path))

        assert (tmp_path / "test-file.dat").read_bytes() == b"file content"

    @pytest.mark.parametrize(
        "filename",
        [
            "../evil.txt",
            "nested/evil.txt",
            r"nested\evil.txt",
            "",
        ],
    )
    def test_download_rejects_path_like_filename_for_directory(self, tmp_path, filename):
        """Test directory downloads reject filenames that could escape the target."""
        file = DummyFile(filename=filename)

        with pytest.raises(ValueError, match="Unsafe filename"):
            file.download(str(tmp_path))

        assert not any(Path(tmp_path).iterdir())


class TestFigureFile:
    """Tests for figure file URL generation."""

    def test_source_path_uses_ftp_images_directory(self):
        """Test figure files use the deposited image path."""
        file = FigureFile(filename="emd_8117.png")
        file._emdb_id = "EMD-8117"

        assert (
            file.source_path
            == "https://ftp.ebi.ac.uk/pub/databases/emdb/structures/EMD-8117/images/emd_8117.png"
        )
