#!/usr/bin/env bash

set -uo pipefail
trap 's=$?; echo "$0: Error on line "$LINENO": $BASH_COMMAND"; exit $s' ERR
IFS=$'\n\t'

root_dir=`sed -nE -e 's|WorkingDirectory=(.+)|\1|p' < /lib/systemd/system/nabd.service`
owner=`stat -c '%U' ${root_dir}`
uid=`stat -c '%u' ${root_dir}`

ci_chroot_test=""
step="init"

for arg in "$@"; do
  if [ "$arg" = "install" ]; then
    step="install"
  elif [ "$arg" = "ci-chroot-test" ]; then
    ci_chroot_test="ci-chroot-test"
  fi
done

case $step in
  "init")
    echo "Stopping services"
    echo "Stopping services" > /tmp/pynab.upgrade
    # stop services using service files.
    for service_file in */*.service ; do
      name=`basename ${service_file}`
      if [ "${name}" != "nabd.service" -a "${name}" != "nabweb.service" ]; then
        sudo systemctl stop ${name} || true
      fi
    done
    sudo systemctl stop nabd.socket || true
    sudo systemctl stop nabd.service || true
  
    echo "Updating Pynab"
    sudo -u ${owner} touch /tmp/pynab.upgrade
    sudo chown ${owner} /tmp/pynab.upgrade
    echo "Updating Pynab - 1/?" > /tmp/pynab.upgrade
    cd ${root_dir}
    if [[ $EUID -ne ${uid} ]]; then
      sudo -u ${owner} git pull
    else
      git pull
    fi

    if printf '%s\n' "${forward_args[@]}" | grep -q "ci-chroot"; then
      bash upgrade.sh --install "${forward_args[@]}"
    else
      bash upgrade.sh --install 
    fi
    echo "Upgrade complete"
    ;;
  "install")
    cd ${root_dir}
    case ci_chroot_test in
        "ci-chroot-test")
          sudo -u ${owner} bash install.sh --upgrade ci_chroot_test
          ;;
        "")
          sudo -u ${owner} bash install.sh --upgrade
          ;;
      esac
    sudo rm -f /tmp/pynab.upgrade
esac
