# generated from gazebo_plugins/env-hooks/gazebo_plugins.sh.in

# detect if running on Darwin platform
_UNAME=`uname -s`
_IS_DARWIN=0
if [ "$_UNAME" = "Darwin" ]; then
  _IS_DARWIN=1
fi
unset _UNAME

if [ $_IS_DARWIN -eq 0 ]; then
  ament_prepend_unique_value LD_LIBRARY_PATH /usr/lib/x86_64-linux-gnu/gazebo-11/plugins
else
  ament_prepend_unique_value DYLD_LIBRARY_PATH /usr/lib/x86_64-linux-gnu/gazebo-11/plugins
fi
unset _IS_DARWIN
