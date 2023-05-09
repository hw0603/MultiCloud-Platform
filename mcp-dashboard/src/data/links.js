import {BsFillBarChartFill, BsFillChatDotsFill} from 'react-icons/bs';
import {HiUserGroup} from 'react-icons/hi';
import {AiFillDatabase, AiTwotoneSetting} from 'react-icons/ai';
import {TbPackageExport} from 'react-icons/tb';
import {FaUserCircle} from 'react-icons/fa';

export const links = [
    {
      title: '메뉴',
      links: [
        {
          name: '대시보드',
          icon: <BsFillBarChartFill />,
        },
        {
          name: '사용자',
          icon: <HiUserGroup />,
        },
        {
          name: '스택',
          icon: <AiFillDatabase />,
        },
        {
          name: '배포',
          icon: <TbPackageExport />,
        },
        {
          name: '작업 로그',
          icon: <BsFillChatDotsFill />,
        },
        {
          name: '활동 로그',
          icon: <BsFillChatDotsFill />,
        },
        {
          name: '설정',
          icon: <AiTwotoneSetting />,
        },
      ],
    },
  
    {
      title: '인증 정보 등록',
      links: [
        {
          name: 'Amazon AWS',
          icon: <FaUserCircle />,
        },
        {
          name: 'Microsoft Azure',
          icon: <FaUserCircle />,
        },
        {
          name: 'Naver NCloud',
          icon: <FaUserCircle />,
        },
      ],
    }
];