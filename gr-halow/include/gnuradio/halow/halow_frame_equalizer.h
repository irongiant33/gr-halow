/*
 * Copyright (C) 2016 Bastian Bloessl <bloessl@ccs-labs.org>
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
 *
 */


#ifndef INCLUDED_HALOW_HALOW_FRAME_EQUALIZER_H
#define INCLUDED_HALOW_HALOW_FRAME_EQUALIZER_H

#include <gnuradio/block.h>
#include <gnuradio/halow/api.h>

namespace gr {
namespace halow {

enum Equalizer {
    LS = 0,
    LMS = 1,
    COMB = 2,
    STA = 3,
    HALOW_LS = 4,
};


class HALOW_API halow_frame_equalizer : virtual public gr::block
{

public:
    typedef std::shared_ptr<halow_frame_equalizer> sptr;
    static sptr make(Equalizer algo, double freq, double bw, bool log, bool debug);
    virtual void set_algorithm(Equalizer algo) = 0;
    virtual void set_bandwidth(double bw) = 0;
    virtual void set_frequency(double freq) = 0;
};

} // namespace halow
} // namespace gr

#endif /* INCLUDED_HALOW_HALOW_FRAME_EQUALIZER_H */