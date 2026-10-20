"""Building height census for a country PBF: how many heights the old 3-storey fallback and
the current tag/type rule assign. Prints the evidence quoted in the 0.4.1 release notes.

    python earthng/height_census.py data/pbf/czech-republic.osm.pbf 20000
"""
import collections
import sys

import osmium

import build_country


def old_height(tags):
    def number(value, default):
        try:
            return float(str(value).split(';')[0].replace(' m', '').replace(',', '.'))
        except (ValueError, TypeError):
            return default
    return max(2.5, min(850., number(tags.get('height'), number(tags.get('building:levels'), 3) * 3)))


def main():
    path = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    stats = {'n': 0, 'old': 0.0, 'new': 0.0, 'changed': 0, 'levels': 0, 'height': 0}
    types = collections.Counter()

    class Handler(osmium.SimpleHandler):
        def way(self, w):
            tags = {k: v for k, v in w.tags}
            if not tags.get('building') or tags['building'] == 'no':
                return
            stats['n'] += 1
            old, new = old_height(tags), build_country.building_height(tags)
            stats['old'] += old
            stats['new'] += new
            stats['changed'] += new != old
            stats['levels'] += 'building:levels' in tags
            stats['height'] += 'height' in tags
            if 'building:levels' not in tags and 'height' not in tags:
                types[tags['building']] += 1
            if stats['n'] >= limit:
                raise SystemExit

    try:
        Handler().apply_file(path, locations=False)
    except SystemExit:
        pass
    n = stats['n']
    print(f'sampled {n} buildings')
    print(f"building:levels {100 * stats['levels'] / n:.1f}%, height {100 * stats['height'] / n:.1f}%")
    print(f"mean {stats['old'] / n:.2f} m -> {stats['new'] / n:.2f} m, {stats['changed']} changed")
    print('untagged types:', types.most_common(10))


if __name__ == '__main__':
    main()
