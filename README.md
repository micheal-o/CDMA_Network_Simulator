# CDMA_Network_Simulator
Admission control is one way cellular networks improve the service provided to their customers in a
mature network. During the initial roll-out of most networks, coverage was the primary goal. Cellular
coverage areas were made as large as possible to minimize the number of cells needed to cover a
population. Most of the time, any user who could attach to a cell would be allowed to do so since the
alternative would usually be a blocked call. However, as networks have matured, there are now
sufficient cells to provide adequate coverage to the vast majority of users, at least in most urban and
suburban areas. Users at or near the edges of most cells usually have a selection of cells any one of
which would provide adequate coverage. Therefore, in a mature network, the emphasis shifts from
providing adequate coverage for each user to providing the highest quality connection to each user.
Quality is directly related to the signal to interference plus noise ratio (SINR) of the received signal. Large
amounts of interference can decrease the SINR and create bit errors in the received signal. For voice
calls, this can cause noticeable noise on the line. For data connections, bit errors will cause
retransmission of data blocks and the network will often compensate by increasing the amount of error
correction bits used, thus decreasing the effective bit rate for data. In both cases, increasing or
persistent interference can cause the connection to be lost entirely.
One way of improving this situation is to put some controls on the admission of users to the network.
Ideally, if a cell is already operating near capacity and the addition of more users would lower
performance for users already connected to the cell, the cell may wish to deny access to the new users
located near the cell boundary since they can presumably find another cell to serve them. This project
simulates the effect of applying an admission control algorithm in a CDMA cell.
