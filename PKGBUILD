# Maintainer: Josh Dagla joshdagla4@gmail.com

pkgname=waybar-tasksys
pkgver=1.0.0
pkgrel=1
pkgdesc="Minimal Rofi-based to-do list module for Waybar"
arch=('any')
url="https://github.com/joshdagla/waybar-tasksys"
license=('MIT')
depends=('python' 'rofi' 'waybar')
source=("$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')

package() {
  install -Dm755 "$srcdir/$pkgname-$pkgver/tasksys.py" "$pkgdir/usr/bin/waybar-tasksys"
  install -Dm644 "$srcdir/$pkgname-$pkgver/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  install -Dm644 "$srcdir/$pkgname-$pkgver/README.md" "$pkgdir/usr/share/doc/$pkgname/README.md"
}
