"""

All rights reserved.

Questions can be directed to support@sunspec.org
"""

import os
import device_das_opal
import das

opal_info = {
    'name': os.path.splitext(os.path.basename(__file__))[0],
    'mode': 'Opal'
}


def das_info():
    return opal_info


def params(info, group_name=None):
    gname = lambda name: group_name + '.' + name
    pname = lambda name: group_name + '.' + GROUP_NAME + '.' + name
    mode = opal_info['mode']
    info.param_add_value(gname('mode'), mode)
    info.param_group(gname(GROUP_NAME), label='%s Parameters' % mode,
                     active=gname('mode'),  active_value=mode, glob=True)
    info.param(pname('target_name'), label='Target name in RT-LAB', default="Target_3")
    info.param(pname('sample_interval'), label='Sample Interval (ms)', default=1000)
    info.param(pname('map'), label='Opal Analog Channel Map', default='Opal_Phase_Jump')
    info.param(pname('model_name'), label='Model Name', default='Opal_Phase_Jump_A_B_A')
    info.param(pname('wfm_dir'), label='Waveform Directory', default='C:\\Users\\DETLDAQ\\OPAL-RT\\'
                                                                     'RT-LABv2019.1_Workspace\\'
                                                                     'IEEE_1547.1_Phase_Jump\\models\\'
                                                                     'Phase_Jump_A_B_A\\phase_jump_a_b_a_sm_source\\'
                                                                     'OpREDHAWKtarget\\')
    info.param(pname('data_name'), label='Waveform Data File Name (.mat)', default='SVP_Data.mat')


GROUP_NAME = 'opal'


class DAS(das.DAS):

    def __init__(self, ts, group_name, points=None, sc_points=None):
        das.DAS.__init__(self, ts, group_name, points=points, sc_points=sc_points)
        self.params['ts'] = ts
        self.params['map'] = self._param_value('map')
        self.params['target_name'] = self._param_value('target_name')
        self.params['sample_interval'] = self._param_value('sample_interval')
        self.params['model_name'] = self._param_value('model_name')
        self.params['wfm_dir'] = self._param_value('wfm_dir')
        self.params['data_name'] = self._param_value('data_name')

        self.device = device_das_opal.Device(self.params)
        self.data_points = self.device.data_points

        # initialize soft channel points
        self._init_sc_points()

        if self.params['sample_interval'] < 50 and self.params['sample_interval'] is not 0:
            raise das.DASError('Parameter error: sample interval must be at least 50 ms or 0 for manual sampling')

    def _param_value(self, name):
        return self.ts.param_value(self.group_name + '.' + GROUP_NAME + '.' + name)


if __name__ == "__main__":

    pass


