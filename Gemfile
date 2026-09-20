source "https://rubygems.org"

# Matches what GitHub Pages runs in production, so a local preview and the
# deployed site build with the same Jekyll and plugin versions. Pinned: older
# releases depend on liquid 4.0.3, which calls String#tainted? and so cannot
# run on Ruby 3.2 or newer.
gem "github-pages", "~> 232", group: :jekyll_plugins

# Not bundled with Ruby 3.4+.
gem "csv"
gem "base64"
gem "bigdecimal"
gem "logger"

# Faster rebuilds for `jekyll serve --livereload` on macOS.
gem "webrick"
