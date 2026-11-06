Name:		jakarta-el
Version:	3.0.3
Release:	1
Summary:	Jakarta Expression Language 3.0 API
Group:		Development/Java
License:	EPL-2.0 or GPLv2 with exceptions
URL:		https://projects.eclipse.org/projects/ee4j.el
Source0:	https://github.com/jakartaee/expression-language/archive/refs/tags/%{version}-RELEASE.tar.gz

BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--alias javax.el:javax.el-api

%description
Expression Language 3.0 API. The Java package is still javax.el.

%prep
%setup -q -n expression-language-%{version}-RELEASE
cp -p LICENSE.md NOTICE.md README.md api/
# Publish the API module only. The ee4j parent POM is not packaged.
python - <<'PY'
import re
import shutil
from pathlib import Path
root = Path(".").resolve()
mod = root / "api"
stage = root.parent / "jakarta-el-module"
if stage.exists():
	shutil.rmtree(stage)
shutil.copytree(mod, stage)
for child in list(root.iterdir()):
	if child.is_dir():
		shutil.rmtree(child)
	else:
		child.unlink()
for child in list(stage.iterdir()):
	shutil.move(str(child), root / child.name)
shutil.rmtree(stage)
pom = Path("pom.xml")
text = pom.read_text()
text = re.sub(r"\s*<parent>.*?</parent>", "", text, count=1, flags=re.S)
text = re.sub(
	r"\s*<resource>\s*<directory>\$\{project\.basedir\}/\.\.</directory>.*?</resource>",
	"",
	text,
	count=1,
	flags=re.S,
)
pom.write_text(text)
PY

%files -f .mfiles
%doc LICENSE.md NOTICE.md README.md
