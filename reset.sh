for file in music/*_archive.txt; do
  [ -f "${file}" ] && rm -- "${file}"
done
