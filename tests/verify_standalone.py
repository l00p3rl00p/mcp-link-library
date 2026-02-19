
import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import os

class TestStandaloneResilience(unittest.TestCase):
    
    def setUp(self):
        # Create a dummy mcp_instance only after modules are mocked
        pass

    def test_missing_dependencies(self):
        print("\n🧪 Testing Standalone Resilience (Missing Dependencies)...")
        
        # Simulate missing optional packages
        with patch.dict(sys.modules, {
            'pypdf': None,
            'openpyxl': None,
            'docx': None,
            'PIL': None,
            'PIL.Image': None
        }):
            # We must reload mcp if it was already imported, or import it fresh
            if 'mcp' in sys.modules:
                del sys.modules['mcp']
            
            # This import should trigger the ImportErrors and set globals to None
            import mcp
            
            # 1. Verify Globals are None
            print("   - Verifying optional imports are handled...")
            self.assertIsNone(mcp.pypdf, "pypdf should be None")
            self.assertIsNone(mcp.openpyxl, "openpyxl should be None")
            self.assertIsNone(mcp.docx, "docx should be None")
            self.assertIsNone(mcp.Image, "PIL.Image should be None")
            print("   ✅ Import degradation confirmed.")
            
            # 2. Verify add_link degradation (PDF)
            print("   - Verifying add_link degradation (PDF)...")
            # Create a dummy PDF file (empty)
            dummy_pdf = Path("standalone_test.pdf")
            dummy_pdf.touch()
            
            try:
                # Initialize Server/Library
                server = mcp.MCPServer()
                # Inject memory DB for testing
                server.library = mcp.SecureMcpLibrary(":memory:")
                
                # Try to add the PDF
                # It should print a warning but NOT crash
                server.library.add_link(f"file://{dummy_pdf.resolve()}", categories=["test"])
                
                # Check if link was added (metadata only)
                links = server.library.list_links()
                self.assertEqual(len(links), 1)
                self.assertIn("standalone_test.pdf", links[0][2]) # Title usually filename
                print("   ✅ PDF added without extractor (Metadata only).")
                
            except Exception as e:
                self.fail(f"❌ Crashed on adding PDF without dependencies: {e}")
            finally:
                if dummy_pdf.exists():
                    dummy_pdf.unlink()
                    
            # 3. Verify add_link degradation (Excel)
            print("   - Verifying add_link degradation (Excel)...")
            dummy_xlsx = Path("standalone_test.xlsx")
            dummy_xlsx.touch()
            try:
                server.library.add_link(f"file://{dummy_xlsx.resolve()}", categories=["test"])
                links = server.library.list_links()
                self.assertEqual(len(links), 2)
                print("   ✅ Excel added without extractor.")
            finally:
               if dummy_xlsx.exists():
                   dummy_xlsx.unlink()

if __name__ == '__main__':
    unittest.main()
