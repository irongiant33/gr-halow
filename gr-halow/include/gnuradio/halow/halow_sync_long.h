/*
 * Copyright (C) 2013, 2016 Bastian Bloessl <bloessl@ccs-labs.org>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
#ifndef INCLUDED_HALOW_HALOW_SYNC_LONG_H
#define INCLUDED_HALOW_HALOW_SYNC_LONG_H

#include <gnuradio/block.h>
#include <gnuradio/halow/api.h>

namespace gr {
namespace halow {

class HALOW_API halow_sync_long : virtual public block
{
public:
    typedef std::shared_ptr<halow_sync_long> sptr;
    static sptr make(unsigned int sync_length, bool log = false, bool debug = false);
};

} // namespace halow
} // namespace gr

#endif /* INCLUDED_HALOW_HALOW_SYNC_LONG_H */