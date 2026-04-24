"""
Dependency Fixer for Destiny
Automatically fixes common dependency issues
Run this if you get any import or version errors
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return success status"""
    try:
        print(f"\n🔧 Running: {command}")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Success")
            if result.stdout:
                print(result.stdout[:200])  # Show first 200 chars
            return True
        else:
            print(f"❌ Failed: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"\n🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and 8 <= version.minor <= 11:
        print("✅ Python version compatible")
        return True
    else:
        print("⚠️  Warning: Python 3.8-3.11 recommended")
        print(f"   You have Python {version.major}.{version.minor}")
        if version.minor >= 12:
            print("   Some packages may have compatibility issues with Python 3.12+")
        return False

def fix_anthropic():
    """Fix anthropic library version issue"""
    print("\n" + "="*50)
    print("🔧 Fixing Anthropic Library (Most Common Issue)")
    print("="*50)
    
    # Uninstall old version
    print("\nStep 1: Removing old version...")
    run_command(f'"{sys.executable}" -m pip uninstall -y anthropic')
    
    # Install latest version
    print("\nStep 2: Installing latest version...")
    success = run_command(f'"{sys.executable}" -m pip install "anthropic>=0.25.0"')
    
    return success

def upgrade_pip():
    """Upgrade pip itself"""
    print("\n🔧 Upgrading pip...")
    return run_command(f'"{sys.executable}" -m pip install --upgrade pip')

def install_requirements():
    """Install all requirements"""
    print("\n" + "="*50)
    print("📦 Installing All Requirements")
    print("="*50)
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        print("   Make sure you're in the project directory")
        return False
    
    success = run_command(f'"{sys.executable}" -m pip install -r requirements.txt')
    
    return success

def verify_installation():
    """Verify all key packages are installed"""
    print("\n" + "="*50)
    print("✓ Verifying Installation")
    print("="*50)
    
    packages = {
        'streamlit': 'Streamlit',
        'anthropic': 'Claude API',
        'sklearn': 'scikit-learn',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'plotly': 'Plotly',
        'requests': 'Requests'
    }
    
    all_good = True
    results = []
    
    for package, name in packages.items():
        try:
            if package == 'sklearn':
                import sklearn
                version = sklearn.__version__
                print(f"✅ {name}: {version}")
                results.append((name, version, True))
            else:
                module = __import__(package)
                version = getattr(module, '__version__', 'unknown')
                print(f"✅ {name}: {version}")
                results.append((name, version, True))
        except ImportError as e:
            print(f"❌ {name}: NOT INSTALLED")
            results.append((name, str(e), False))
            all_good = False
        except Exception as e:
            print(f"⚠️  {name}: {str(e)[:50]}")
            results.append((name, str(e)[:50], False))
            all_good = False
    
    return all_good, results

def test_imports():
    """Test key Destiny imports"""
    print("\n" + "="*50)
    print("🧪 Testing Destiny Components")
    print("="*50)
    
    tests = [
        ('config', 'Config'),
        ('memory', 'Memory'),
        ('evaluator', 'Evaluator'),
        ('data_manager', 'DataManager'),
        ('ml_models', 'MarketingPredictor'),
        ('content_generator', 'ContentGenerator'),
    ]
    
    all_good = True
    
    for module_name, class_name in tests:
        try:
            module = __import__(module_name)
            getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
        except ImportError as e:
            print(f"❌ {module_name}: File not found")
            all_good = False
        except AttributeError as e:
            print(f"⚠️  {module_name}: Class {class_name} not found")
            all_good = False
        except Exception as e:
            print(f"❌ {module_name}: {str(e)[:50]}")
            all_good = False
    
    return all_good

def main():
    print("="*50)
    print("🎯 Destiny Dependency Fixer")
    print("="*50)
    
    # Check Python version
    check_python_version()
    
    # Upgrade pip first
    print("\nStep 0: Upgrading pip...")
    upgrade_pip()
    
    # Fix anthropic first (most common issue)
    print("\nStep 1: Fixing Claude API library...")
    fix_anthropic()
    
    # Install all requirements
    print("\nStep 2: Installing all dependencies...")
    install_success = install_requirements()
    
    # Verify
    print("\nStep 3: Verifying installation...")
    verify_success, results = verify_installation()
    
    # Test imports
    print("\nStep 4: Testing Destiny components...")
    import_success = test_imports()
    
    # Summary
    print("\n" + "="*50)
    if verify_success and import_success:
        print("✅ ALL DEPENDENCIES INSTALLED SUCCESSFULLY!")
        print("="*50)
        print("\n🚀 You're ready to run Destiny!")
        print("\n   Run this command:")
        print("   streamlit run app.py")
        print("\n   Or:")
        print("   python -m streamlit run app.py")
    else:
        print("⚠️  SOME ISSUES DETECTED")
        print("="*50)
        
        if not verify_success:
            print("\n❌ Missing packages:")
            for name, info, success in results:
                if not success:
                    print(f"   - {name}")
        
        if not import_success:
            print("\n❌ Some Destiny components couldn't be imported")
            print("   Make sure all .py files are in the same directory")
        
        print("\n📖 Try these solutions:")
        print("   1. Make sure you're in the project directory")
        print("   2. Use a virtual environment:")
        print("      python -m venv venv")
        print("      source venv/bin/activate  # Linux/Mac")
        print("      venv\\Scripts\\activate     # Windows")
        print("      python fix_dependencies.py")
        print("\n   3. Manual install:")
        print("      pip install --no-cache-dir -r requirements.txt")
        print("\n   4. Check TROUBLESHOOTING.md for more help")
    
    print("\n")

if __name__ == "__main__":
    main()