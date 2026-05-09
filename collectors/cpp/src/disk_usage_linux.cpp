#include "disk_usage.h"
#include <sys/statvfs.h>
#include <optional>

std::optional<double> DiskUsage::get_disk_percent() {
    struct statvfs stat;

    if (statvfs("/", &stat) != 0)
        return std::nullopt;

    unsigned long total = stat.f_blocks * stat.f_frsize;
    unsigned long free  = stat.f_bfree  * stat.f_frsize;

    if (total == 0) return std::nullopt;

    double used = (double)(total - free);
    double percent = (used / (double)total) * 100.0;

    return percent;
}
